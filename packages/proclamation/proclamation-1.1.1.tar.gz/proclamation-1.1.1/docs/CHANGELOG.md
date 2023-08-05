# Changelog for Proclamation, the changelog combiner

<!--
SPDX-License-Identifier: CC0-1.0
SPDX-FileCopyrightText: 2020 Collabora, Ltd. and the Proclamation contributors
-->

## Proclamation 1.1.1 (2020-07-28)

This adds one major new feature (`sort_by_prefix`), a public JSON schema, and a
variety of smaller improvements.

(Version 1.1.0 was briefly tagged but never published to PyPI, 1.1.1 replaces it
entirely.)

- Script
  - Add section setting `sort_by_prefix` to allow optionally sorting by a colon-
    delimited prefix in fragment text (or the first word if no colon exists).
    ([!16](https://gitlab.com/ryanpavlik/proclamation/merge_requests/16))
  - Report an error if a project name is specified but not found in the config
    file, and add tests for `ProjectCollection`.
    ([!18](https://gitlab.com/ryanpavlik/proclamation/merge_requests/18),
    [#12](https://gitlab.com/ryanpavlik/proclamation/issues/12))
- Templates
  - Start fragment references on a new line, and only place one reference per line
    (manually wrapped). This keeps the wrapping filter from mangling the Markdown-
    formatted links.
    ([!15](https://gitlab.com/ryanpavlik/proclamation/merge_requests/15))
- Misc
  - docs: Mention the emerging practice of starting your fragment with a component,
    subsection, or change type (feature or bug fix), followed by a colon, like this
    entry.
    ([!15](https://gitlab.com/ryanpavlik/proclamation/merge_requests/15))
  - Improve API documentation.
    ([!16](https://gitlab.com/ryanpavlik/proclamation/merge_requests/16))
  - Add more tests for `Project`, `Fragment` (including parsing from disk), and
    `SectionSettings`.
    ([!16](https://gitlab.com/ryanpavlik/proclamation/merge_requests/16))
  - Add a JSON Schema for config files. To use, add
    `"$schema": "https://ryanpavlik.gitlab.io/proclamation/proclamation.schema.json"`
    to the root of your config file. Some editors will use this to provide
    editing help.
    ([!17](https://gitlab.com/ryanpavlik/proclamation/merge_requests/17))
  - The name of the default branch has been changed to `main`.

## Proclamation 1.0.2.2 (2020-03-23)

Packaging release: no functional change if you run from source or have your own
template. Otherwise, upgrade recommended.

- Fix `MANIFEST.in` to properly package the base template.

## Proclamation 1.0.2.1 (2020-03-18)

Brown-paper-bag release: no functional change, no need to upgrade from 1.0.2.

- Fix reuse.software metadata. No functional change.
  ([!14](https://gitlab.com/ryanpavlik/proclamation/merge_requests/14))

## Proclamation 1.0.2 (2020-03-18)

- Script
  - Remove redundant code from reference parsing, and improve docstrings/doctests.
    ([!8](https://gitlab.com/ryanpavlik/proclamation/merge_requests/8))
  - Sort fragments in each section based on the tuple-ized form of their first
    reference (from the filename). This will keep MR's in a section in numerical
    order, etc. ([!9](https://gitlab.com/ryanpavlik/proclamation/merge_requests/9),
    [#4](https://gitlab.com/ryanpavlik/proclamation/issues/4))
  - Error out if we can't parse a front-matter line as a reference, instead of
    silently swallowing the error.
    ([!11](https://gitlab.com/ryanpavlik/proclamation/merge_requests/11))
  - Support comment lines in per-fragment (YAML-like) front matter: a line with `#`
    followed by anything, optionally preceded by whitespace.
    ([!11](https://gitlab.com/ryanpavlik/proclamation/merge_requests/11),
    [#8](https://gitlab.com/ryanpavlik/proclamation/issues/8))
- Templates
  - No significant changes
- Misc
  - Adjust copyright and license notices, placing documentation, config file, and
    templates under CC0-1.0 so they may be re-used in other projects that use
    Proclamation.
    ([!7](https://gitlab.com/ryanpavlik/proclamation/merge_requests/7))
  - Changes to ensure compliance with version 3.0 of the
    [REUSE](https://reuse.software) specification as well as [standard-
    readme](https://github.com/RichardLitt/standard-readme)
    ([!7](https://gitlab.com/ryanpavlik/proclamation/merge_requests/7))
  - Split some content from `README.md` into a `USAGE.md` designed for reuse in
    projects that use Proclamation.
    ([!7](https://gitlab.com/ryanpavlik/proclamation/merge_requests/7))
  - Add Sphinx documentation, connected to read-the-docs.
    ([!8](https://gitlab.com/ryanpavlik/proclamation/merge_requests/8))
  - Update `setup.py` to specify that we need `click` version 7.
    ([!10](https://gitlab.com/ryanpavlik/proclamation/merge_requests/10),
    [#7](https://gitlab.com/ryanpavlik/proclamation/issues/7))
  - Fix spelling errors/typos, and add `codespell` to tox and CI.
    ([!12](https://gitlab.com/ryanpavlik/proclamation/merge_requests/12),
    [#6](https://gitlab.com/ryanpavlik/proclamation/issues/6))
  - Start testing against Python 3.8 as well.
    ([!13](https://gitlab.com/ryanpavlik/proclamation/merge_requests/13))
  - Note in USAGE that you can append a `.2`, `.3`, etc. before the extension of a
    filename if you want more than one changelog item for a single "main"
    reference.
    ([!13](https://gitlab.com/ryanpavlik/proclamation/merge_requests/13))

## Proclamation 1.0.1 (2020-03-04)

- Script
  - Handle missing directories more carefully. If a directory is found to be
    missing during `draft`, we continue with a warning, skipping only that
    project. However, if a directory is found to be missing during `build`, we
    error out and modify no changelogs.
    ([!1](https://gitlab.com/ryanpavlik/proclamation/merge_requests/1))
  - Fix remove-fragments subcommand.
    ([#1](https://gitlab.com/ryanpavlik/proclamation/issues/1),
    [!4](https://gitlab.com/ryanpavlik/proclamation/merge_requests/4))
  - Fix the functioning of the `--delete-fragments` option of the `build`
    subcommand. ([!5](https://gitlab.com/ryanpavlik/proclamation/merge_requests/5),
    [#2](https://gitlab.com/ryanpavlik/proclamation/issues/2))
  - Ensure that a new changelog portion always ends with a blank line.
    ([!6](https://gitlab.com/ryanpavlik/proclamation/merge_requests/6),
    [#3](https://gitlab.com/ryanpavlik/proclamation/issues/3))
  - Pass project `base_url` from settings to template. (bug fix)
    ([!2](https://gitlab.com/ryanpavlik/proclamation/merge_requests/2))
- Templates
  - Fix a number of issues with the base template: missed leftover renaming errors,
    spacing errors, duplicated parentheses around references.
    ([!3](https://gitlab.com/ryanpavlik/proclamation/merge_requests/3))
  - Further fix spacing in default template, and add a test for correct behavior of
    the template in simple scenarios.
    ([!6](https://gitlab.com/ryanpavlik/proclamation/merge_requests/6),
    [#3](https://gitlab.com/ryanpavlik/proclamation/issues/3))

## Proclamation 1.0.0 (2020-02-24)

Initial release.
