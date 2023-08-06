import sys
from optparse import OptionParser
from typing import Set, List, Any
from pathlib import Path

from gitlab import GitlabAuthenticationError, GitlabUpdateError

from mkmr.instance import Instance
from mkmr.utils import strtobool, msg, warn, err

from . import __version__

# Store all valid values in a set we can check for validity
# we also print them after some processing for the user so
# they know what attributes of a merge request they can modify
# and what kind of input (boolean, string, integer, etc...) each
# attribute takes
VALID_VALUES: Set[str] = {
    "assignee_id",
    "assignee_ids",
    ":description",
    "description",
    "description:",
    ":labels",
    "labels",
    "labels:",
    "milestone_id",
    "remove_source_branch",
    "state_event",
    "target_branch",
    ":title",
    "title",
    "title:",
    "discussion_locked",
    "squash",
    "allow_collaboration",
    "allow_maintainer_to_push",
}


def set_attribute(object, key: str, value: Any, quiet: bool):
    """Set the value of a key in a dict, print a message if not quiet

    Args:
        object ([type]): the dict we should modify
        key (str): the key we should modify
        value (Any): the value we should put in the key
        quiet (bool): true to print a message, false to not print anything
    """
    if not quiet:
        msg("{} -> {}".format(key, value))
    setattr(object, key, value)


def print_values():
    """Print valid values along with its expected values"""
    for val in iter(VALID_VALUES):
        if (
            val == "remove_source_branch"
            or val == "squash"
            or val == "discussion_locked"
            or val == "allow_collaboration"
            or val == "allow_maintainer_to_push"
        ):
            print("{} -> boolean".format(val))
        elif val == "assignee_id":
            print("{} -> integer".format(val))
        elif val == "assignee_ids":
            print("{} -> multiple integers separated by whitespace".format(val))
        elif val == "labels" or val == ":labels" or val == "labels:":
            print("{} -> one or more strings separated by whitespace".format(val))
        else:
            print("{} -> a single string".format(val))


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
        help="Show which values would be changed but not change them",
    )
    parser.add_option(
        "--timeout",
        dest="timeout",
        action="store",
        type="int",
        help="Set timeout for making calls to the gitlab API",
    )
    parser.add_option(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        help="Don't print warnings of invalid values",
    )
    parser.add_option(
        "-v",
        "--verbose",
        dest="quiet",
        action="store_false",
        help="Print warnings of invalid values",
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
        help="which remote to operate on",
    )
    parser.add_option(
        "-l",
        "--list",
        dest="list",
        action="store_true",
        help="Show list of attributes that can be modified",
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
        quiet=None,
        save=False,
        list=False,
        clean_branch_cache=False,
        reset_project_id=False,
    )

    (options, args) = parser.parse_args(sys.argv)

    if options.list is True:
        print_values()
        sys.exit(0)

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
        err("no merge request given")
        sys.exit(1)

    if len(args) < 3:
        err("no attributes to edit given")
        sys.exit(1)

    # Annotate some variables
    cachepath: Path  # Path to where the branch files are
    # Number of the internal-id or branch name that has a cache file with the internal-id
    # of the merge request
    mrnum: str

    mrnum = args[1]

    if not mrnum.isdigit():
        try:
            cachepath = remote.cache.branches / mrnum
            mrnum = cachepath.read_text()
        except FileNotFoundError:
            err("branch name given, {}, has no corresponding cache file".format(mrnum))
            sys.exit(1)
        else:
            # This is executed in a try-catch if there are no exceptions raised
            if mrnum == "":
                err("cache file for {} is empty".format(mrnum))
                cachepath.unlink()  # Delete the file as it is empty
                sys.exit(1)

    project = remote.gitlab.projects.get(
        remote.api.projectid, retry_transient_errors=True, lazy=True
    )
    mr = project.mergerequests.get(mrnum, include_rebase_in_progress=True)

    # Annotate some variables
    key: str  # Key given to us in 'KEY=VAL'
    val: str  # Value given to us in 'KEY=VAL'

    for arg in args[2:]:

        key = arg.split("=")[0]
        if key not in VALID_VALUES:
            continue
        try:
            val = arg.split("=")[1]
        except IndexError:
            continue

        # Check if we are passing a valid type
        if (
            key == "remove_source_branch"
            or key == "squash"
            or key == "discussion_locked"
            or key == "allow_collaboration"
            or key == "allow_maintainer_to_push"
        ):
            if strtobool(val) is None:
                if not options.quiet:
                    warn("value of {} ({}), is invalid, should be True or False".format(key, val))
                continue
        elif key == "state_event":
            if val != "close" and val != "reopen":
                if not options.quiet:
                    warn(
                        "value of {} ({}), is invalid, should be either close or reopen".format(
                            key, val
                        )
                    )
                continue
        elif key == "assignee_id" or key == "milestone_id":
            # "" and 0 are the same thing for the GitLab API, it justs allows us to try a conversion
            # to int
            if val == "":
                val = "0"

            # Check if are not a digit and complain if --quiet is not passed
            if not val.isdigit():
                if not options.quiet:
                    warn("value of {} ({}), is invalid, should be an integer".format(key, val))
            else:
                set_attribute(mr, key, int(val), options.quiet)

            # We should continue at the end of this clause because we are doing setattr
            # ourselves instead of relying on the setattr at the end of the loop
            continue
        elif key == "title":
            if val == mr.attributes["title"]:
                if not options.quiet:
                    warn("value of title hasn't changed")
                continue
            if val == "":
                if not options.quiet:
                    warn("value of title should not be empty")
                continue
        elif key == ":title" or key == "title:":
            if val == "":
                if not options.quiet:
                    warn("value of title should not be empty")
                continue
            if key == ":title":
                val = "{} {}".format(val, mr.attributes["title"])
            elif key == "title:":
                val = "{} {}".format(mr.attributes["title"], val)
            key = "title"
        elif key == "description":
            if len(val) > 1048576:
                if not options.quiet:
                    warn("description has more characters than limit of 1048576")
                continue
        elif key == ":description" or key == "description:":
            if len(val) + len(mr.attributes["description"]) > 1048576:
                if not options.quiet:
                    warn("description has more characters than limit of 1048576")
                continue
            if key == ":description":
                val = "{} {}".format(val, mr.attributes["description"])
            elif key == "description:":
                val = "{} {}".format(mr.attributes["description"], val)
            key = "description"
        elif key == "labels":
            if not val.split():
                if not options.quiet:
                    warn("No labels were passed")
                    continue
            set_attribute(mr, key, val.split(), options.quiet)

            # We should continue at the end of this clause because we are doing setattr
            # ourselves instead of relying on the setattr at the end of the loop
            continue
        elif key == ":labels" or key == "labels:":
            if not val.split():
                if not options.quiet:
                    warn("No labels were passed")
                    continue
            o: List[str] = mr.attributes["labels"]
            for val in val.split():
                o.append(val)
            set_attribute(mr, key, o, options.quiet)

            # We should continue at the end of this clause because we are doing setattr
            # ourselves instead of relying on the setattr at the end of the loop
            continue
        elif key == "assignee_ids":
            # "" and 0 are the same thing for the GitLab API, it justs allows us to try a conversion
            # to int
            if not val:
                int_v = 0

            # Create an empty list that will hold all the IDs that we were given
            # and are valid
            list_v: List[int] = []

            # Split the values given by whitespace and try to convert them to int
            # if we cannot convert then complain if --quiet is not set, and if we
            # can convert, add them to our List[str]
            for value in val.split():
                try:
                    int_v = int(value)
                except ValueError:
                    if not options.quiet:
                        warn("key {} has invalid sub-value {} in value {}".format(key, value, val))
                else:
                    list_v.append(int_v)

            # Small check, we don't want to be setting an empty list, if the user
            # legitimately passed nothing then a single int 0 is passed which for
            # gitlab is the same thing as ""
            if list_v:
                set_attribute(mr, key, list_v, options.quiet)

            # We should continue at the end of this clause because we are doing setattr
            # ourselves instead of relying on the setattr at the end of the loop
            continue

        # We reached the end of the loop, hopefully the correct if-clause was reached
        # for the key given to us and the proper transformations were done.
        # Use set_attribute to change the value of the key in the object.
        set_attribute(mr, key, val, options.quiet)

    try:
        mr.save()
    except GitlabAuthenticationError as e:
        err("Failed to update, authentication error\n\n{}".format(e))
    except GitlabUpdateError as e:
        err("Failed to update, update error\n\n{}".format(e))


if __name__ == "__main__":
    main()
