# Proclamation

[![pipeline status](https://gitlab.com/ryanpavlik/proclamation/badges/main/pipeline.svg)](https://gitlab.com/ryanpavlik/proclamation/-/commits/main)
[![coverage report](https://gitlab.com/ryanpavlik/proclamation/badges/main/coverage.svg)](https://gitlab.com/ryanpavlik/proclamation/-/commits/main)
[![Documentation Status](https://readthedocs.org/projects/proclamation/badge/?version=latest)](https://proclamation.readthedocs.io/en/latest/?badge=latest)
[![REUSE status](https://api.reuse.software/badge/gitlab.com/ryanpavlik/proclamation)](https://api.reuse.software/info/gitlab.com/ryanpavlik/proclamation)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)
[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

A tool for building CHANGES/NEWS files from fragments.

Inspired by [towncrier][], but completely language-agnostic and markup-agnostic.
(The default template uses markdown, but all formatting is controlled by Jinja2
templates so you can change that as desired.)

Maintained at <https://gitlab.com/ryanpavlik/proclamation>

Documentation also available at <https://proclamation.readthedocs.io/en/latest/>

[towncrier]: https://github.com/hawkowl/towncrier

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
  - [CLI](#cli)
- [Maintainers](#maintainers)
- [Thanks](#thanks)
- [Code of Conduct](#code-of-conduct)
- [Contributing](#contributing)
- [License](#license)
  - [Default license, including all Python code files](#default-license-including-all-python-code-files)
  - [Templates and this documentation](#templates-and-this-documentation)

## Background

The concept behind [towncrier][] is great: ease the maintenance burden of
creating human-readable changelogs (for projects where a git log/shortlog won't
suffice) and simultaneously

- have each contributor/change author describe their own change for a
  human-readable changelog
- avoid merge conflicts from everyone editing the same changelog file

Towncrier, as well as Proclamation, do this by having "changelog fragments"
accumulate between releases, and combining them (with a template and some
metadata) when running the tool before a release. While towncrier is focused on
Python and `.rst` formatting, Proclamation is explicitly language-neutral (a
motivating use case was a mixed-content repo with specifications as well as C++
code) and markup-neutral (all formatting is done by a Jinja2 template: the
default is markdown but you can complete change the formatting if you supply a
custom template.)

## Install

**Note:** Contributors to your Proclamation-using project do not need to install
Proclamation -- all they have to do is create a text file, and only the person
doing releases strictly needs to install Proclamation. However, there are some
utilities that they might find useful if they do.

Proclamation is available on [pypi][], so you can install it for your local user with:

```sh
pip3 install --user proclamation
```

Updating to a new release would be done with

```sh
pip3 install --user --upgrade proclamation
```

Alternately, you can install from this repository. If you do this, it's
recommended to install this in a virtualenv. Something like this will work on
*nix-like systems, adjusted for your shell usage.

```bash
# Create a virtualenv in `venv`
python3 -m venv venv

# Activate it
. venv/bin/activate

# Install a link to this package in the venv.
pip install --editable .
```

If you follow those instructions, the virtualenv will refer to the source
instead of copying the source, so updating your local clone of this repo will
also update the virtualenv. Omit the `--editable` if you want other behavior.

Note that the `venv/bin/proclamation` script can be run from outside the venv,
through the magic of setuptools, so if you want to be able to use it elsewhere
on your system, you might symlink it into a directory that's in your `PATH`.

[pypi]: https://pypi.org/project/proclamation/

## Usage

For detailed instructions that you might consider copying and modifying for your
own project, see [USAGE.md](USAGE.md).

Proclamation itself is primarily used through the command line by the person
making releases.

If the `proclamation` command line tool doesn't quite suit your complex needs,
you can access the bulk of the functionality through using this as a Python
module. See the command line interface driver, `proclamation/main.py`, to see
how it interacts with the underlying capabilities.

### CLI

Proclamation has command-line help available by passing `--help`. You can access
general help, listing overall options and subcommands, as follows:

```sh
proclamation --help
```

Additionally, each subcommand has its own help text, describing it and its available options, for example:

```sh
proclamation build --help
```

A brief description of the two most common subcommands follows.

To see a preview of the changelog additions that would be made if you
released a new version right now, run

```sh
proclamation draft
```

The `draft` subcommand is the most useful one to non-maintaining contributors
who choose to install Proclamation, as it lets them verify their changelog
fragment(s) appear as desired.

The main subcommand used by maintainers is `build`, for example like this:

```sh
proclamation build YOUR_VERSION_NUMBER_HERE --delete-fragments --overwrite
```

This command updates your changelog file(s) (overwriting the original), and
removes your used changelog fragments for you. (You still need to remove them
from your version control system.)

## Maintainers

[@ryanpavlik](https://gitlab.com/ryanpavlik)

## Thanks

This tool was initially developed by Ryan Pavlik in the course of his work at
the open-source software consultancy [Collabora](https://collabora.com). Thanks
to Collabora and their "Open First" mantra for supporting the development of
this software.

A debt of gratitude is owed to the developers of the [towncrier][] package,
which strongly inspired the usage pattern for this tool. (Before writing this
tool, Ryan initially attempted to modify towncrier to suit the use cases he
had.) It's definitely a project worth looking into if you maintain a Python
project. (The Proclamation project doesn't use it, despite being in Python,
because it uses itself...) Ryan first learned about towncrier at
[Stephen Finucane's talk at FOSDEM 2020](https://fosdem.org/2020/schedule/event/python2020_manage_change/).

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By
participating in this project you agree to abide by its terms.

## Contributing

If you have questions or found a bug, feel free to file an issue on the GitLab
project for Proclamation.

Merge requests are gratefully accepted. To develop on Proclamation, you'll
probably want to follow the virtualenv installation instructions above to
locally install a link in a virtualenv.

Additionally, consider the following suggestions/requirements:

- Run `pytest-3` or similar to run the automated tests.
- Run `autopep8 proclamation/*.py proclamation/test/*.py --in-place` to
  automatically format the source code with [autopep8][].
- Use [`tox`][tox] to run [flake8][] as well as tests for multiple Python versions.
  - e.g. on Debian Buster, you can run `tox -e py37,flake8` (adding `py35` if
    you upgraded from Stretch and never removed python 3.5)
- When submitting a change, be sure to create your changelog fragment in the
  changes directory! :)
- If editing the README, please conform to the
  [standard-readme](https://github.com/RichardLitt/standard-readme)
  specification.

No copyright assignment is required to contribute. However, you are required to
make your contributions available under the prevailing license for that content
type (see below) for it to be accepted into the main repo.

[tox]: https://tox.readthedocs.io/en/latest/
[flake8]: https://flake8.pycqa.org/en/latest/
[autopep8]: https://github.com/hhatto/autopep8.

## License

The *tl;dr* is: The bulk of the package is [Apache-2.0][] licensed. Files that
you might incorporate into your own project are [CC0][] (public domain
dedication or nearest equivalent based on jurisdiction); this is so you can
freely use them into your project no matter what license you use.

Every file has an SPDX license tag and copyright or author information in it
which should be considered the authoritative licensing data.

Note that dependencies and third-party documents may have their own licenses.
For instance, the code of conduct, based on the Contributor Covenant v2.0, is
licensed CC-BY-4.0.

This project is [REUSE-compliant](https://reuse.software) (version 3.0 of the
REUSE specification). You can use that project's tools to work with copyright
and licenses of files in this project.

[Apache-2.0]: http://www.apache.org/licenses/LICENSE-2.0
[CC0]: https://creativecommons.org/publicdomain/zero/1.0/

### Default license, including all Python code files

```txt
Copyright 2019-2020 Collabora, Ltd. and the Proclamation contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

### Templates and this documentation

```txt
SPDX-License-Identifier: CC0-1.0
SPDX-FileCopyrightText: 2020 Collabora, Ltd. and the Proclamation contributors
```

- This `README.md` file
- `proclamation/templates/*`

[CC0 1.0 Universal (CC0 1.0) Public Domain Dedication][CC0]

```txt
To the extent possible under law, the person who associated CC0 with this work
has waived all copyright and related or neighboring rights to this work. This
work is published from: United States.
```
