#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd. and the Proclamation contributors
#
# SPDX-License-Identifier: Apache-2.0

from copy import deepcopy

from ..project import Project
from ..settings import parse_project
from .test_settings import PROJECT


def test_project_and_section_create():
    proj_config = deepcopy(PROJECT)
    print(repr(proj_config))
    proj_settings = parse_project(proj_config)
    proj = Project(proj_settings)
    assert(len(proj.sections) == 1)
    assert(proj.sections[0].name == "main section")
    assert(proj.sections[0].relative_directory ==
           "changes/main")
    assert(proj.sections[0].sort_by_prefix is False)


def test_project_and_section_create_sort_by_prefix():
    proj_config = deepcopy(PROJECT)
    proj_config["sections"]["main section"]["sort_by_prefix"] = True
    print(repr(proj_config))
    proj_settings = parse_project(proj_config)
    proj = Project(proj_settings)
    assert(len(proj.sections) == 1)
    assert(proj.sections[0].name == "main section")
    assert(proj.sections[0].relative_directory ==
           "changes/main")
    assert(proj.sections[0].sort_by_prefix is True)
