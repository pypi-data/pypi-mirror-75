#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd. and the Proclamation contributors
#
# SPDX-License-Identifier: Apache-2.0

from ..project import Project
from ..render import (combine_changelogs, get_split_news_file, render_template,
                      split_news_contents)
from ..settings import ProjectSettings, SectionSettings

NEWS_FILE_1 = """# Sample NEWS file

## Test 1.0 (date goes here)

## Previous

## More previous

"""


def test_split_news():
    proj_settings = ProjectSettings("Test")
    before, after = split_news_contents(proj_settings, NEWS_FILE_1)
    assert("Sample" in before)
    assert("Previous" in after)
    assert(after.startswith("##"))


def make_dummy_project_settings():
    proj_settings = ProjectSettings("Test", news_filename="nonexistent-file")
    return proj_settings


def make_dummy_project_settings_with_sections():
    proj_settings = make_dummy_project_settings()
    proj_settings.sections.append(
        SectionSettings("Features", "missing-dir/features"))
    proj_settings.sections.append(
        SectionSettings("Bug fixes", "missing-dir/bugs"))
    return proj_settings


def test_missing_news_file():
    proj_settings = make_dummy_project_settings()
    before, after = get_split_news_file(proj_settings)
    assert(after == "")
    assert(before.endswith("\n"))


def test_duplicated_version():
    proj_settings = make_dummy_project_settings()
    before, after = split_news_contents(proj_settings, NEWS_FILE_1)
    assert("Test 1.0" in after)
    project = Project(proj_settings)
    try:
        combine_changelogs(before, after, project, "1.0", "date goes here")
    except RuntimeError:
        assert(True)
        return
    assert(False)  # We expect an error.


EXPECTED1 = """## Test 1.0 (Release Date)

"""


def test_render_no_sections():
    proj_settings = make_dummy_project_settings()
    project = Project(proj_settings)
    rendered = render_template(project, "1.0", "Release Date")
    assert(rendered.endswith("\n\n"))
    assert(rendered.startswith("## Test 1.0 (Release Date)\n\n"))
    assert(EXPECTED1 == rendered)


EXPECTED2 = """## Test 1.0 (Release Date)

- Features
  - No significant changes
- Bug fixes
  - No significant changes

"""


def test_render_no_fragments():
    proj_settings = make_dummy_project_settings_with_sections()
    project = Project(proj_settings)
    rendered = render_template(project, "1.0", "Release Date")
    assert(rendered.endswith("\n\n"))
    assert(rendered.startswith("## Test 1.0 (Release Date)\n\n"))
    assert(EXPECTED2 == rendered)
