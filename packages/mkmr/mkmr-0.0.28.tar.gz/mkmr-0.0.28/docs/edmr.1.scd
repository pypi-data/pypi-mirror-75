edmr(1)

# NAME

edmr - Programmatically edit attributes of merge requests

# SYNOPSIS

*edmr* [options] <MRNUM> <commands...>

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
	Show which values would be changed but not change them

*--timeout* <TIMEOUT>
	Set timeout for making calls to the gitlab API

*-q, --quiet*
	Don't print warnings of invalid values

*-v, --verbose*
	Print warnings of invalid values

*--save*
	If any value option is passed, save it to configuration

*--remote* <REMOTE>
	which remote to operate on

*-l, --list*
	Show list of attributes that can be modified

*--reset-project-id*
	Remove project-id file in cache, required when the GitLab project changes its internal-id

*--clean-cached-branches*
	Remove dangling references in branch cache (empty files and ones without a local branch)

# DESCRIPTION

edmr is a python3 script that allows an user to edit attributes of the merge
requests that are allowed by the gitlab v4 API.

It can be used programmatically from a shellscript or from the command-line.

it makes uses of an ini-format configuration file to store the url of the
instance and the personal access token used to interact with the GitLab API of
the hosted instance. And it uses information stored in the git repository in
the form of remotes to guess which GitLab instance it should interact with.

# EXAMPLES

## Setting a title

```
edmr 1000 title="This is a new title"
```

## Appending or Prefixing a title

```
edmr 1000 :title="This comes before"
edmr 1000 title:="This comes after"
```

# CONFIGURATION

edmr will aggressively try to create a configuration file in the following path
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

edmr will read the files written in cache, as described in mkmr-cache(7), to
stablish a connection between a branch and what merge request has that branch
as its source.
