vimr(1)

# NAME

vimr - Interactively edit attributes of merge requests like git rebase -i

# SYNOPSIS

*vimr* [options] <MRNUM...>

# OPTIONS

*--version*
	Show version number and quit

*-h, --help*
	Show help message and quit

*--token* <TOKEN>
	GitLab Personal Access Token

*-c, --config* <CONFIG>
	Full path to configuration directory

*-n, --dry-run*
	Show which values would be changed

*--timeout* <TIMEOUT>
	Set timeout for making calls to the gitlab API

*--save*
	If any value option is passed, save it to configuration

*--remote* <REMOTE>
	Which remote to operate on

*-q, --quiet*
	Print only unrecoverable errors

*-v, --verbose*
	Print recovered errors and warnings

*--reset-project-id*
	Remove project-id file in cache, required when the GitLab project changes its internal-id

*--clean-cached-branches*
	Remove dangling references in branch cache (empty files and ones without a local branch)

# DESCRIPTION

vimr is a python3 script that allows an user to edit attributes of the merge
requests that are allowed by the gitlab v4 API.

it makes uses of an ini-format configuration file to store the url of the
instance and the personal access token used to interact with the GitLab API of
the hosted instance. And it uses information stored in the git repository in
the form of remotes to guess which GitLab instance it should interact with.

# CONFIGURATION

vimr will aggressively try to create a configuration file in the following path
under certain conditions:

. $XDG_CONFIG_HOME/mkmr/config (if XDG_CONFIG_HOME is set)
. $HOME/.config/mkmr/config (if XDG_CONFIG_HOME is not set)

The configuration is an ini-format with the same sections, keys and values as
used by python-gitlab.

Example configuration:

```
[gitlab.alpinelinux.org]
url = https://gitlab.alpinelinux.org
private_token = 123456789abcdefg
```

# CACHE

vimr will read the files written in cache, as described in mkmr-cache(7), to
stablish a connection between a branch and what merge request has that branch
as its source.
