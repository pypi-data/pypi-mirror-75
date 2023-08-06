import sys
from json import dumps
from optparse import OptionParser
from time import sleep
from pathlib import Path
from typing import Dict, List, Any

from git import GitCommandError
from gitlab import GitlabMRClosedError, GitlabMRRebaseError

from mkmr.instance import Instance
from mkmr.utils import msg, warn, err

from . import __version__


def main():
    parser = OptionParser(version=__version__)
    parser.add_option(
        "--token", dest="token", action="store", type="string", help="GitLab Personal Access Token"
    )
    parser.add_option(
        "-c",
        "--config",
        dest="config",
        action="store",
        type="string",
        help="Full path to configuration directory",
    )
    parser.add_option(
        "-n",
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Show which merge requests mgmr would try to merge",
    )
    parser.add_option(
        "--timeout",
        dest="timeout",
        action="store",
        type="int",
        help="Set timeout for making calls to the gitlab API",
    )
    parser.add_option(
        "--save",
        dest="save",
        action="store_true",
        help="If any value option is passed, save it to configuration",
    )
    parser.add_option(
        "--remote",
        dest="remote",
        action="store",
        type="string",
        help="Which remote to operate on",
    )
    parser.add_option(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        help="Print only the json with the results or in case of an unrecoverable error",
    )
    parser.add_option(
        "-v",
        "--verbose",
        dest="quiet",
        action="store_false",
        help="Print results and recovered errors",
    )
    parser.add_option(
        "-w",
        "--wait",
        dest="wait",
        action="store",
        type="int",
        help="Interval between pings to GitLab to see if Merge Request was rebased",
    )
    parser.add_option(
        "--clean-cached-branches",
        dest="clean_branch_cache",
        action="store_true",
        help="Remove branch files that are empty or don't match a local branch",
    )
    parser.add_option(
        "--reset-project-id",
        dest="reset_project_id",
        action="store_true",
        help="Remove project-id cache file (needed if the project changes its internal id)",
    )
    parser.set_defaults(
        token=None,
        config=None,
        remote=None,
        timeout=None,
        wait=None,
        quiet=None,
        save=False,
        clean_branch_cache=False,
        reset_project_id=False,
    )

    (options, args) = parser.parse_args(sys.argv)

    try:
        remote = Instance(options, offline=options.clean_branch_cache)
    except (ValueError, AttributeError) as e:
        err(e)
        sys.exit(1)
    except Instance.ProjectIdReset:
        msg("Reset project-id for remote '{}'".format(options.remote))
    except Instance.BranchNoCache:
        warn("No branch cache for remote '{}'".format(options.remote))
    except Instance.BranchNothingCleaned:
        msg("Nothing in the cache needs to cleaned for remote '{}'".format(options.remote))
    except Instance.BranchCacheCleaned:
        msg("Removed dangling branch references for remote '{}'".format(options.remote))

    if options.clean_branch_cache or options.reset_project_id:
        sys.exit(0)

    if len(args) < 2:
        err("no merge requests given")
        sys.exit(1)

    project = remote.gitlab.projects.get(
        remote.api.projectid, retry_transient_errors=True, lazy=True
    )

    # Annotate some variables
    queue: Dict[str, str]  # A Dictionary of {merge request: its status}
    n: int  # Which member we are, this is checked against keys_len to not go out of index
    keys: List[str]  # List of strings that hold the 'merge request' from 'queue'
    keys_len: int  # How many keys we have

    """
    Create a dictionary that is our queue of merge requests to work on, they have the following
    scheme of {'MRNUM': 'STATE'}, the state can be one of the 3:
    - pending (this means the merge request needs to be processed)
    - merged (this means the merge request was merged, the best outcome)
    - any value other than the 2 above is an error and needs to be inspected by the user

    errors can happen for many reasons, not enough permissions to merge or to rebase, rebase failed
    because of conflicts, etc.

    also create a list of the keys we have, those are the ones we will iterate over in our workloop,
    and get the length of the list so we know when we have processed all the merge requests.
    """
    queue = dict()
    n = 0
    for arg in args[1:]:
        queue[arg] = "pending"

    keys = list(queue.keys())
    keys_len = len(keys)

    if options.dry_run is True:
        msg("MRs to be merged: {}".format(" ".join(keys)))
        sys.exit(0)

    """
    This is a loop that iterates over all members of our queue dictionary using a needle that
    starts at 0 and will break the loop once the needle value gets higher than the length of
    our dictionary

    This is the logic of our loop:
    1. Get the merge request
    2. Check a few attributes of the merge request
       a. if the value of the 'state' key is 'merged', then set the merge request as
          'already merged' in the dictionary, increment the needle and restart the loop
       b. if the value of the 'state' key is 'closed', then set the merge request as 'closed' in
          the dictionary, increment the needle and restart the loop
       c. if the key 'work_in_progress' is True, then set the merge request as 'work in progress'
          in the dictionary, increment the needle and restart the loop
       d. if the key 'rebase_in_progress' is True, sleep for 2 seconds and restart the loop
       e. if the key 'rebase_in_progress' is False and 'merge_error' attribute is not null, then
          set the merge request in the dictionary as the value of the 'merge_error' key, increment
          the needle and restart the loop
    2. Try merging it
       a. if merging fails with error code 406, try starting a rebase request
          i. if asking for a rebase fails with error code 403, then set the merge request as
             'Rebase failed:' with the error message, increment the needle and restart the loop
          ii. if asking for a rebase returns 202, restart the loop
       b. if it fails with error code 401, then set the merge request as 'Merge failed:' with the
          error message, increment the needle and restart the loop
       c. if it works, then set the merge request as 'merged', increment the needle and restart the
          loop
    """
    # Annotate some variables
    name: str  # Number (or name) of the merge request we are merging
    cachepath: Path  # Path to the branch cache file is
    iid: int  # Number of the merge request
    present: str  # The string that represents the merge request, either number or branch(number)

    # Dictionary from GitLab, taken from the status of a merge request, we can't know the types
    # of what they give, and it can be anything ranging from 'str' to 'Dict[Dict[Any, Any], Any]
    attrs: Dict[Any, Any]

    while True:

        # This will be reached once we have worked on all members
        if n + 1 > keys_len:
            break

        # Set our needle in the list, k can be either the name of a branch of the internal id of a
        # merge request
        name = keys[n]
        cachepath = remote.cache.branches / name
        if cachepath.is_file():
            # If it is a file then try to read it and convert it to an integer at the same
            # time, there is the possibility of a FileNotFoundError but it is very unlikely
            try:
                iid = int(cachepath.read_text())
            except ValueError:
                # We reach here if the user has a cache file, we can read it, but the
                # value in it is not valid (not int), so check if the name of branch
                # given to us is *actually* an integer itself and try to use it, this deals
                # with the potential problem of someone having a branch literally called '123'
                # and they actually want to merge the MR with internal-id '123'
                if not options.quiet:
                    warn(
                        "File has invalid value '{}', it must be an integer".format(
                            cachepath.read_text()
                        )
                    )
                    cachepath.unlink()  # Delete the file as it has an invalid value
                if name.isdigit():
                    iid = int(name)
                    present = name
                else:
                    queue[name] = "Invalid: branch name has an incorrect or empty cache file"
                    n += 1
                    continue
            else:
                # the way we represent the internal id for printing, in this case we do
                # branch_name(internal_id), if we reached here then we have a valid cache
                present = "{}({})".format(name, iid)
        else:
            if name.isdigit():
                iid = int(name)
                present = name
            else:
                queue[name] = "Invalid: string given for merge request is not integer"
                n += 1
                continue

        """
        Get the merge request, include_rebase_in_progress is required so
        we get information on whether we are rebasing
        """
        mr = project.mergerequests.get(iid, include_rebase_in_progress=True)

        attrs = mr.attributes
        if attrs["state"] == "merged":
            if not options.quiet:
                warn("{} is already merged".format(present))
            if present != name:  # This means we are using the branch cache file
                cachepath.unlink()
            queue[name] = "Merge: already merged"
            n += 1
            continue
        elif attrs["state"] == "closed":
            if not options.quiet:
                warn("{} is closed".format(present))
            if present != name:  # This means we are using the branch cache file
                cachepath.unlink()
            queue[name] = "Merge: closed"
            n += 1
            continue
        elif attrs["work_in_progress"] is True:
            if not options.quiet:
                warn("{} is a work in progress, can't merge".format(present))
            queue[name] = "Merge: work in progress"
            n += 1
            continue
        elif attrs["rebase_in_progress"] is True:
            if not options.quiet:
                msg(
                    "{} is currently rebasing".format(present)
                    + ", waiting {} seconds to check if it still rebasing".format(options.wait)
                )
            sleep(options.wait)
            continue
        elif attrs["rebase_in_progress"] is False and attrs["merge_error"] is not None:
            if not options.quiet:
                err("{} {}".format(present, attrs["merge_error"]))
            queue[name] = "Rebase: " + attrs["merge_error"]
            n += 1
            continue

        try:
            mr.merge(should_remove_source_branch="true")
        except GitlabMRClosedError as e:
            if e.response_code == 406:
                if not options.quiet:
                    msg("{} cannot be merged, trying to rebase".format(present))
                try:
                    # Passing skip_ci actually doesn't work for some reason
                    # so a new CI Pipeline is always created unfortunately
                    #
                    # TODO: Find out why it doesn't work
                    mr.rebase(skip_ci=True)
                except GitlabMRRebaseError as ee:
                    if ee.response_code == 403:
                        if not options.quiet:
                            err("Rebase failed: {}".format(ee.error_message))
                        queue[name] = "Rebase: " + ee.error_message
                        n += 1
                        continue
                else:
                    continue
            elif e.response_code == 401:
                if not options.quiet:
                    err("Merge failed: {}".format(e.error_message))
                queue[name] = "Merge: " + e.error_message
                n += 1
                continue
            elif e.response_code == 405:
                if not options.quiet:
                    err("Merge failed: {}".format(e.error_message))
                queue[name] = "Merge: " + e.error_message
                n += 1
            else:
                err("{} aborting completely".format(e.error_message))
                sys.exit(1)
        else:
            if not options.quiet:
                msg("Merged {}".format(present))
            queue[name] = "merged"
            # Switch to master if our current branch is the active branch
            if name != str(iid):
                if name == remote.repo.active_branch.name:
                    remote.repo.git.checkout("master")
                remote.repo.git.branch("-D", name)
            if present != name:  # This means we are using branch file
                cachepath.unlink()
            n += 1

    print(dumps(queue, indent=4))


if __name__ == "__main__":
    main()
