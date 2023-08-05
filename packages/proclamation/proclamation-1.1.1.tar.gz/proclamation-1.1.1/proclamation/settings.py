#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd. and the Proclamation contributors
#
# SPDX-License-Identifier: Apache-2.0
"""Project settings."""

import logging
import re

from .types import ReferenceParser

_LOG = logging.getLogger(__name__)


class SectionSettings:
    """Settings for a single :class:`Section`."""

    def __init__(self, name, directory, sort_by_prefix=False):
        """Construct a section settings object."""
        self.name = name
        """Section name."""

        self.directory = directory
        """Directory containing changelog fragments for this section."""

        self.sort_by_prefix = sort_by_prefix
        """Whether fragments should be sorted by first word before rendering.

        This would be a stable sort that preserves the reference sort for same
        first words."""

        _LOG.debug("Created: %s", repr(self))

    def __repr__(self):
        """Return a representation of this object.

        >>> repr(SectionSettings('Name', 'mydir'))
        "SectionSettings('Name', 'mydir', False)"

        >>> repr(SectionSettings('Name', 'mydir', False))
        "SectionSettings('Name', 'mydir', False)"

        >>> repr(SectionSettings('Name', 'mydir', True))
        "SectionSettings('Name', 'mydir', True)"
        """
        return "SectionSettings({}, {}, {})".format(
            repr(self.name), repr(self.directory), repr(self.sort_by_prefix)
        )


class ProjectSettings:
    """Settings for an entire :class:`Project`.

    Often parsed from JSON with a similar structure.
    """

    def __init__(self, project_name, template=None, base_url=None,
                 insert_point_pattern=None,
                 news_filename=None, extra_data=None):
        """Construct a settings object."""
        self.name = project_name
        """Name of the project."""

        # We do the None testing here, instead of having a more meaningful
        # default above, because a config file might pass us "None" for
        # all of these.
        if template is None:
            template = "base.md"
        self.template = template
        """Filename of the changelog template."""

        self.sections = []
        """List of :class:`SectionSettings` objects."""

        self.base_url = base_url
        """Base URL of project management.

        This is your project URL if using GitHub or GitLab with the default
        template."""

        if insert_point_pattern is None:
            insert_point_pattern = r'^## .*'
        self.insert_point_re = re.compile(insert_point_pattern)
        """A regular expression matching the line we should insert before,
        compiled from ``insert_point_pattern``."""

        if news_filename is None:
            news_filename = "NEWS"
        self.news_filename = news_filename
        """The filename of your NEWS/CHANGES file."""

        if extra_data is None:
            extra_data = {}
        self.extra_data = extra_data
        """Extra data for use by your template."""

    def make_reference_parser(self, base_dir=None):
        """Make a :class:`ReferenceParser`.

        This is an expansion point for further usage, if projects
        end up needing to supply a custom reference parser without
        having to replace the rest of the command-line infrastructure, etc.
        """
        parser = ReferenceParser()
        return parser


class Settings:
    """Top-level settings class.

    Often parsed from JSON with a similar structure.
    """

    def __init__(self):
        """Construct a top-level settings."""
        self.projects = []
        """List of :class:`ProjectSettings` objects."""

    def add_project(self, project_settings):
        """Add a :class:`ProjectSettings` object to this settings."""
        self.projects.append(project_settings)


def parse_section(section_name, section_info):
    """Parse a name and dictionary into a :class:`SectionSettings` object."""
    return SectionSettings(section_name,
                           section_info["directory"],
                           section_info.get("sort_by_prefix", False))


def parse_project(proj):
    """Parse a dictionary into a :class:`ProjectSettings` object."""
    proj_settings = ProjectSettings(
        project_name=proj["project_name"],
        template=proj.get("template"),
        base_url=proj.get("base_url"),
        insert_point_pattern=proj.get("insert_point_pattern"),
        news_filename=proj.get("news_filename"),
        extra_data=proj.get("extra_data"))
    for section_name, section_info in proj["sections"].items():
        proj_settings.sections.append(
            parse_section(section_name, section_info))
    return proj_settings


def parse_settings(config):
    """Parse settings from a dict into a :class:`Settings` object."""
    settings = Settings()
    # Having multiple projects at top level is optional.
    projects = config.get("projects")
    if projects:
        for project in projects:
            settings.add_project(parse_project(project))
    else:
        settings.add_project(parse_project(config))
    return settings


def settings_from_json_io(io):
    """Load :class:`Settings` from json in an IO like a file or
    :class:`StringIO`."""
    import json
    config = json.load(io)
    return parse_settings(config)


def settings_from_json_file(fn):
    """Load :class:`Settings` from a JSON file."""
    with open(str(fn), 'r', encoding='utf-8') as fp:
        return settings_from_json_io(fp)
