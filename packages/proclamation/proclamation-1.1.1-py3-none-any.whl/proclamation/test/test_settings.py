#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd. and the Proclamation contributors
#
# SPDX-License-Identifier: Apache-2.0

import json
from io import StringIO

from ..settings import parse_project, parse_section, settings_from_json_io

PROJ_NAME = "my project"

PROJECT = {
    "project_name": PROJ_NAME,
    "template": "dummy",
    "sections": {
        "main section": {
            "directory": "changes/main"
        }
    }
}


def dict_to_json_io(config):
    return StringIO(json.dumps(config))


def test_parse_project():
    proj = parse_project(PROJECT)
    assert(proj.name == PROJ_NAME)


def test_single_project():
    config = {
        "projects": [
            PROJECT
        ]
    }
    io = dict_to_json_io(config)
    settings = settings_from_json_io(io)
    assert(len(settings.projects) == 1)
    assert(settings.projects[0].name == PROJ_NAME)
    assert(settings.projects[0].template == "dummy")
    assert(len(settings.projects[0].sections) == 1)

# def test_multi_project():
#     pass


def test_project_toplevel():
    io = dict_to_json_io(PROJECT)
    settings = settings_from_json_io(io)
    assert(len(settings.projects) == 1)
    assert(settings.projects[0].name == PROJ_NAME)
    assert(settings.projects[0].template == "dummy")
    assert(len(settings.projects[0].sections) == 1)


def test_parse_section():
    sect_setting_dict = {
        "directory": "changes/main"
    }

    sect = parse_section("main section", sect_setting_dict)
    assert(sect.name == "main section")
    assert(sect.directory == sect_setting_dict['directory'])
    assert(sect.sort_by_prefix is False)

    sect_setting_dict['sort_by_prefix'] = True
    sect = parse_section("main section", sect_setting_dict)
    assert(sect.name == "main section")
    assert(sect.directory == sect_setting_dict['directory'])
    assert(sect.sort_by_prefix is True)
