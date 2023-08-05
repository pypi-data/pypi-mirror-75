#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd. and the Proclamation contributors
#
# SPDX-License-Identifier: Apache-2.0

import tempfile
from pathlib import Path
import json
import pytest

from ..main import ProjectCollection
from .test_settings import PROJECT, PROJ_NAME


def create_config_file(dirname, config_json):
    our_dir = Path(dirname)
    fn = str(our_dir / '.proclamation.json')
    with open(fn, 'w') as fp:
        json.dump(config_json, fp)
    return fn


def test_named_project():
    with tempfile.TemporaryDirectory() as dirname:
        fn = create_config_file(dirname, PROJECT)
        collection = ProjectCollection(fn, PROJ_NAME, dirname)
        assert(len(collection.projects) == 1)


def test_all_projects():
    with tempfile.TemporaryDirectory() as dirname:
        fn = create_config_file(dirname, PROJECT)
        collection = ProjectCollection(fn, None, dirname)
        assert(len(collection.projects) == 1)


def test_missing_project():
    with tempfile.TemporaryDirectory() as dirname:
        fn = create_config_file(dirname, PROJECT)
        with pytest.raises(Exception):
            _ = ProjectCollection(fn, "Incorrect Project", dirname)
