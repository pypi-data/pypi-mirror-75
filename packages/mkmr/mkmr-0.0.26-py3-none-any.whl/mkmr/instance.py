from os import getenv
from git import Repo
from gitlab import Gitlab
from typing import Optional
from pathlib import Path


# Helper functions that can only be used in this file
def init_repo(path=None) -> Repo:
    from git import InvalidGitRepositoryError

    # If no path is given to us, assume they want the repo from the
    # current working directory
    if not path:
        path = Path.cwd()

    try:
        repo = Repo(path)
    except InvalidGitRepositoryError:
        if path == Path("/"):
            raise
        return init_repo(path=path.parent)
    else:
        return repo

    try:
        return init_repo(path)
    except InvalidGitRepositoryError:
        raise ValueError(
            "Failed to start repo at {} or any of its parent directories".format(path)
        )


def create_dir(path: Path) -> Path:
    """Create or re-create a directory with 700 permissions, and its parents

    Args:
        path (Path): full path to the directory to be created

    Returns:
        Path: full path to the directory that was created
    """
    if path.exists() and not path.is_dir():
        path.unlink()

    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    return path


def create_file(path: Path) -> Path:
    """Create a file or re-creates it with 600 permissions, create parent directories with 700
    permissions

    Args:
        path (Path): full path to the file to be created

    Returns:
        Path: full path to the file that was created
    """
    # Get the parent
    create_dir(path.parent)

    # If the file exists but is not a file then remove
    # it is as well
    if path.exists() and not path.is_file():
        path.unlink()

    # Create it with nice permissions for a file that
    # hold secrets
    path.touch(mode=0o600)
    return path


class Instance:
    """
    Superclass that holds all classes that one needs to interact with mkmr, you can
    instantiante this only once and then call the proper subclass and its members
    """

    class BranchCacheCleaned(Exception):
        """This is raised after the branch cache is cleaned (all dangling references
        and empty files removed), you can catch this and sys.exit(0)
        """

    class BranchNoCache(Exception):
        """This is raised if we ask to clean the branch cache, but it has no cache
        to be cleaned, in this case the user should be told there is nothing to clean
        """

    class BranchNothingCleaned(Exception):
        """This is raised if we ask to clean the branch cache, and we check the files
        in the cache and none of them need to be cleaned, we should tell the user
        that nothing needs to be cleaned or that the cache is already cleaned
        """

    class ProjectIdReset(Exception):
        """This is raised after the project id is reset (project-id file removed),
        you can catch this and sys.exit(0)
        """

    def reset_project_id(self):
        if self.cache.project_id.exists():
            self.cache.project_id.unlink()
        raise self.ProjectIdReset

    def clean_branch_cache(self):
        from git import GitCommandError
        from os import listdir
        from os.path import getsize

        from mkmr.utils import msg

        # Annotate some variables
        filepath: Path  # Path to the branch cache file
        has_cleaned: bool = False  # If true, we cleaned stuff up
        if not self.cache.branches.is_dir():
            raise self.BranchNoCache
        for branch in listdir(self.cache.branches):
            filepath = self.cache.branches / branch
            # If the files are empty they are of no use to us, just remove them
            if getsize(filepath) == 0:
                msg("removed: {} (empty file)".format(filepath))
                filepath.unlink()
                has_cleaned = True
                continue
            try:
                self.repo.git.rev_parse("--verify", branch)
            except GitCommandError:
                msg("removed: {} (no local branch)".format(filepath))
                filepath.unlink()
                has_cleaned = True
        if has_cleaned:
            raise self.BranchCacheCleaned
        else:
            raise self.BranchNothingCleaned

    def __init__(self, options, remote=None, offline=False):
        """Initialize everything for the Instance object, except if offline=True is passed
        then initialize everything but not what is required to interface with GitLab, we
        allow that for cases where only local operations are done

        Args:
            options (OptParser): Objects with all parsed options we can deal with
            remote (optional): String that is the remote we want to interact with. Defaults to None.
            offline (bool, optional): Whether to perform network operations. Defaults to False.
        """
        # Initialize our repo object based on the local repo we have
        try:
            self.repo = init_repo()
        except ValueError:
            raise

        reader = self.repo.config_reader(config_level="repository")

        if not remote:
            if hasattr(options, "remote"):
                remote = options.remote
                if not remote:
                    remote = reader.get_value("mkmr", "upstream", default="upstream")
            else:
                remote = reader.get_value("mkmr", "origin", default="origin")

        writer = self.repo.config_writer(config_level="repository")
        if hasattr(options, "remote"):
            writer.set_value("mkmr", "upstream", remote)
        else:
            writer.set_value("mkmr", "origin", remote)
        writer.release()

        self.remote = remote
        self.api = self.API(self.repo, remote=remote)

        # If we are not offline (that means )
        if options.overwrite and not options.token:
            raise ValueError("--overwrite requires --token to be passed")
        self.config = self.Config(options, self.api.domain)
        self.cache = self.Cache(self.api.domain.replace("/", "."), self.api.user, self.api.project)

        if hasattr(options, "reset_project_id"):
            if options.reset_project_id:
                self.reset_project_id()

        if hasattr(options, "clean_branch_cache"):
            if options.clean_branch_cache:
                self.clean_branch_cache()

        # Only run the following code if the user expects us to do operations online
        # if the user is simply passing --clean-cache then there is no reason to
        # perform **potentially** expensive operations like querying the project-id
        # (it can not be cached, even though it is cached aggressively).
        #
        # While the getting of self.gitlab is purely offline there is also the possibility
        # that it will fail and offline operations don't need GitLab.
        if not offline:
            # Start a GitLab configuration by loading from the function get_gitlab()
            # which is defined in the 'config' class
            self.gitlab = Gitlab.from_config(self.api.domain, [self.config.path])
            # If the user passed --token to us then override the token acquired
            # from private_token
            if options.token:
                self.gitlab.private_token = options.token
            # If the user passed --timeout to us then override the token acquired
            # from timeout or the default value
            if options.timeout:
                self.gitlab.timeout = options.timeout

            # Set the value of projectid from API by calling the load_project_id, which needs
            # to access the Cache object
            self.api.projectid = self.load_project_id(self.gitlab)

    class API:
        domain: str  # Domain. Example: gitlab.alpinelinux.org
        projectid: int  # ID of the Project. Example: 1
        user: str  # User of the Project. Example: alpine
        project: str  # Name of the Project. Example: aports

        def __init__(self, repo: Repo, remote: str):
            from giturlparse import parse

            """
            Check that we were given a valid remote
            """
            if remote in repo.remotes:
                uri = repo.remotes[remote].url
            else:
                raise ValueError(
                    "We were passed the remote '{}' which does not exist in the repository".format(
                        remote
                    )
                )

            """
            Parse the url with giturlparse and check what values we got from it
            """
            p = parse(uri)
            self.domain = p.domain

            try:
                "".join(["https://", self.domain])
            except AttributeError:
                raise AttributeError(
                    "url from remote '{}' has no valid URL: {}".format(remote, uri)
                )
            try:
                # Some people have a remote that is
                # git@gitlab.alpinelinux.org:/User/Project.git
                # The / in /User causes problems when using pathlib, so strip it here to avoid any
                # future problems
                if p.owner[0] == "/":
                    p.owner = p.owner[1:]
                self.user = p.owner
            except AttributeError:
                raise AttributeError(
                    "url from remote '{}' has no component owner in its url: '{}'".format(
                        remote, uri
                    )
                )
            try:
                self.project = p.repo
            except AttributeError:
                raise AttributeError(
                    "url from remote '{}' has no repo component in its url: '{}'".format(
                        remote, uri
                    )
                )

    class Config:
        path: Path

        def __init__(self, options, domain: str):
            from configparser import SafeConfigParser
            from os.path import basename
            from sys import argv

            xdgpath: Optional[str]  # Value of XDG_CONFIG_HOME, can be none if unset
            homepath: Optional[str]  # Value of HOME, required if xdgpath is None

            if options.config:
                path = Path(options.config)
                self.path = create_file(path)

            if not options.config:
                xdgpath = getenv("XDG_CONFIG_HOME")
                if xdgpath is not None:
                    path = Path(xdgpath)
                    self.path = create_file(path / "mkmr" / "config")

                if xdgpath is None:
                    homepath = getenv("HOME")
                    if homepath is None:
                        raise ValueError(
                            "Neither XDG_CONFIG_HOME or HOME are set, please set XDG_CONFIG_HOME"
                        )

                    if xdgpath is None:
                        path = Path(homepath)
                        self.path = create_file(path / ".config" / "mkmr" / "config")

            """
                Write the configuration passed to us via the CLI to the config
                file if it's not there already or the user wants to overwrite it
            """
            parser = SafeConfigParser()
            parser.read(self.path)

            if parser.has_section(domain) is False:
                parser.add_section(domain)

            # In case the 'url' options is not set in the section we are looking for
            # then just write it out.
            if parser.has_option(domain, "url") is False:
                parser[domain]["url"] = "https://" + domain

            if not parser.has_option(domain, "private_token") or options.overwrite is True:
                # If --token is not passed to us then drop out with a long useful
                # message, if it is passed to us write it out in the configuration
                # file
                if options.token is None:
                    raise ValueError(
                        "Visit https://"
                        + domain
                        + "/profile/personal_access_tokens to generate your token\n\n"
                        + "Then run {} with --token <TOKEN>".format(basename(argv[0]))
                    )
                else:
                    parser[domain]["private_token"] = options.token

            # Write to configuration only at the end, so we don't have malformed
            # sections in case things fail
            with open(self.path, "w") as c:
                parser.write(c)

    class Cache:
        # Combination of $domain/$user/$project to separate caches for different
        # projects
        namespace: Path

        cachedir: Path  # Full path to the cache directory
        project_id: Path  # Full path to the project-id file
        branches: Path  # Full path to the branches directory

        def __init__(self, domain: str, user: str, project: str):
            self.namespace = Path() / domain / user / project

            # Annotate some variables
            xdgpath: Optional[str]  # Value of XDG_CACHE_HOME, can be none if unset
            homepath: Optional[str]  # Value of HOME, required if xdgpath is None

            xdgpath = getenv("XDG_CACHE_HOME")
            if xdgpath is not None:
                path = Path(xdgpath)
                self.cachedir = create_dir(path / "mkmr")

            if xdgpath is None:
                homepath = getenv("HOME")
                if homepath is None:
                    raise ValueError(
                        "Neither XDG_CACHE_HOME or HOME are set, please set XDG_CACHE_HOME"
                    )

                if homepath is not None:
                    path = Path(homepath)
                    self.cachedir = create_dir(path / ".cache" / "mkmr")

            self.project_id = self.cachedir / self.namespace / "project-id"
            self.branches = self.cachedir / self.namespace / "branches"

    def load_project_id(self, gitlab: Gitlab) -> int:
        # The path should be, as an example taking alpine/aports from gitlab.alpinelinux.org
        # $XDG_CACHE_HOME/mkmr/gitlab.alpinelinux.org/alpine/aports/project-id
        cachepath = self.cache.project_id
        if cachepath.is_file():
            self.projectid = int(cachepath.read_text())
            return self.projectid
        """
        Call into the gitlab API to get the project id
        """
        from urllib.request import Request, urlopen
        import json

        req = Request(
            self.gitlab.api_url + "/projects/" + self.api.user + "%2F" + self.api.project
        )
        req.add_header("Private-Token", self.gitlab.private_token)
        f = urlopen(req).read()
        j = json.loads(f.decode("utf-8"))
        cachepath.write_text(str(j["id"]))
        self.projectid = j["id"]
        return self.projectid
