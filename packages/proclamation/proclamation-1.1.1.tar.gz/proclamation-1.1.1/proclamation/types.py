#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd. and the Proclamation contributors
#
# SPDX-License-Identifier: Apache-2.0

import logging
from operator import attrgetter
from pathlib import Path

_LOG = logging.getLogger(__name__)

FRONT_MATTER_DELIMITER = "---"


class Reference:
    """A simple class storing the information about a reference.

    A reference is an issue, merge/pull request, ticket number, etc: any known
    namespace of identifiers that suit your project. By customizing your
    template (or, in extreme cases, your reference parser) you can accommodate
    a variety of project structures split across multiple systems.

    Generally created from a string by :class:`ReferenceParser`.

    If you customize Proclamation by writing your own customized subclass
    of :class:`ReferenceParser`, you do not necessarily have to use this
    class. However, for most project structures, even fairly complicated ones,
    this class and a custom template suffice.
    """

    def __init__(self, item_type, number, service_params):
        """Construct from a parsed reference string."""
        super().__init__()

        self.item_type = item_type
        """Item type, like ``issue``, ``mr``, ``pr``."""

        self.number = number
        """Reference number."""

        self.service_params = service_params
        """A list/tuple of any additional parameters associated with the
        service."""

    def as_tuple(self):
        """Return all contents as a tuple for use in sets and maps.

        Required of all classes that are to be used as a reference,
        for de-duplication.

        Don't actually use this in your templates!
        """
        return (self.item_type, self.number, tuple(self.service_params))

    def __repr__(self):
        return "Reference({}, {}, {})".format(repr(self.item_type),
                                              repr(self.number),
                                              repr(self.service_params))


class ReferenceParser:
    """The base class and default "reference parser".

    If you choose to customize this functionality, inherit from it.
    Otherwise, use it as-is.

    Reference parsers may use the :class:`Reference` class from this module,
    as this one does, but it's not required.
    Whatever suits you best is fine as long as it works with your template.

    References are things like ticket numbers, issue numbers, merge/pull
    request numbers, etc. This portion of the system is left fairly flexible
    since there are almost as many project administration structures as there
    are projects.
    """

    def __init__(self):
        """Construct parser."""
        self.extensions_to_drop = set(('md', 'rst', 'txt'))

    def split_on_dot_and_drop_ext(self, s):
        """Return the .-delimited portions of a name/ref, excluding a file extension,
        and whether or not a file extension was removed.

        This is a utility function used by both :func:`parse` and
        :func:`parse_filename`.

        >>> ReferenceParser().split_on_dot_and_drop_ext("mr.50.md")
        (['mr', '50'], True)

        >>> ReferenceParser().split_on_dot_and_drop_ext("mr.50.extradata.md")
        (['mr', '50', 'extradata'], True)

        >>> ReferenceParser().split_on_dot_and_drop_ext("mr.50")
        (['mr', '50'], False)

        >>> ReferenceParser().split_on_dot_and_drop_ext("mr.50.extradata")
        (['mr', '50', 'extradata'], False)
        """
        elts = s.split(".")
        if elts[-1] in self.extensions_to_drop:
            elts.pop()
            return elts, True
        return elts, False

    def make_reference(self, elts):
        """Convert a list/tuple of elements into a reference.

        This might be the only function you need to override if you need a
        custom reference parser but can deal with the filename being
        ``.``-delimited.

        Called by :func:`parse_filename` and :func:`parse` once they've
        separated the parts of their input string.

        >>> ReferenceParser().make_reference(['mr', '50', 'extradata'])
        Reference('mr', 50, ['extradata'])

        >>> ReferenceParser().make_reference(['mr', '50'])
        Reference('mr', 50, [])

        >>> ReferenceParser().make_reference(['mr', '50', 'extradata',
        ...                                   'evenmoredata'])
        Reference('mr', 50, ['extradata', 'evenmoredata'])

        This list is not a valid reference: not enough elements.

        >>> ReferenceParser().make_reference(['mr'])

        This list is not a valid reference: can't convert the second element
        to a number.

        >>> ReferenceParser().make_reference(['mr', 'fifty'])

        """
        if len(elts) < 2:
            # Only one component: Can't be a ref.
            return None
        try:
            return Reference(item_type=elts[0],
                             number=int(elts[1]),
                             service_params=elts[2:])
        except ValueError:
            # Conversion failure, etc. means this isn't actually a ref
            return None

    def parse_filename(self, s):
        """Turn a filename string into a reference or None.

        Unlike :func:`parse`, this method requires that the string end in one
        of the known file extensions, as a way to avoid accidentally loading
        files that aren't meant to be changelog fragments.

        May override or extend.


        >>> ReferenceParser().parse_filename("mr.50.md")
        Reference('mr', 50, [])

        >>> ReferenceParser().parse_filename("mr.50.extradata.md")
        Reference('mr', 50, ['extradata'])

        This should return None because there's no file extension.

        >>> ReferenceParser().parse_filename("mr.50")

        This should return None because there's no (recognized) file extension.

        >>> ReferenceParser().parse_filename("mr.50.extradata")
        """
        elts, removed_extension = self.split_on_dot_and_drop_ext(s)
        if not removed_extension:
            # Filenames must have the extension
            return None

        if elts and not elts[0]:
            # Empty first component: not a valid ref file.
            return None
        return self.make_reference(elts)

    def parse(self, s):
        """Turn a string into a reference or None.

        This will drop a file extension if it's present, but does not require
        it to be present unlike :func:`parse_filename`.

        May override or extend.


        >>> ReferenceParser().parse("mr.50.md")
        Reference('mr', 50, [])

        >>> ReferenceParser().parse("mr.50.extradata.md")
        Reference('mr', 50, ['extradata'])

        >>> ReferenceParser().parse("mr.50")
        Reference('mr', 50, [])

        >>> ReferenceParser().parse("mr.50.extradata")
        Reference('mr', 50, ['extradata'])
        """
        elts, _ = self.split_on_dot_and_drop_ext(s)

        return self.make_reference(elts)


class Fragment:
    """A single CHANGES/NEWS entry, provided as text to insert into the templates.

    A fragment comes from a file or stream.

    The fragment filename is parsed to provide one reference. Optionally, an
    extremely small subset of "YAML front matter" can be used to list
    additional references in the fragment file contents. Delimit the front
    matter with --- both before and after, and place one reference per line
    (with or without leading -) between those delimiters.
    """

    ARBITRARY_MAX_PREFIX_LEN = 40
    """If the first colon in a fragment is after this many characters or more,
    we assume it's not actually the prefix. It may instead be, for example,
    a URL included in the fragment text.
    """

    def __init__(self, filename, reference=None, ref_parser=None, io=None):
        """Construct a fragment.

        Filename is used to open the file, if io is not provided.
        ref_parser parses "reference" strings (referring to PR/MR/issue) into
        a reference object.
        A default is provided.
        For testing or advanced stuff, pass a file handle or something like
        StringIO to io, in which case filename is not used.
        """
        super().__init__()
        filename = Path(filename)
        self.filename = filename
        self.text = ""
        self.io = io
        if ref_parser is None:
            ref_parser = ReferenceParser()
        self._ref_parser = ref_parser

        if not reference:
            reference = ref_parser.parse_filename(filename.name)
        self._ref = reference

        self.refs = []
        """All references added for a fragment, including the first.

        Do not modify manually."""

        self._known_refs = set()
        """The set of all ref tuples associated with this fragment.

        Do not modify manually."""
        self._insert_ref(reference)

        self._prefix = None

    def _insert_ref(self, reference):
        ref_tuple = reference.as_tuple()
        if ref_tuple not in self._known_refs:
            self.refs.append(reference)
            self._known_refs.add(ref_tuple)

    def __lt__(self, other):
        """Compare less-than for fragment sorting."""
        # For now - sort based on the first reference of a fragment.
        # This is typically the one from the filename.
        return self.ref.as_tuple() < other.ref.as_tuple()

    @property
    def ref(self):
        """Get the first reference used for a fragment, which becomes an ID."""
        return self._ref

    def _populate_prefix(self):
        """Cache the computed prefix."""
        if not self.text:
            return
        if self._prefix:
            return
        # First try splitting on colon.
        parts = self.text.split(':', maxsplit=1)
        if len(parts) == 2 and len(parts[0]) < self.ARBITRARY_MAX_PREFIX_LEN:
            self._prefix = parts[0]
            return
        # If that fails, just do spaces.
        parts = self.text.split(' ', maxsplit=1)
        self._prefix = parts[0]

    @property
    def prefix(self):
        """Get the colon-delimited prefix or first word of the content."""
        if not self.text:
            return ''
        self._populate_prefix()
        return self._prefix

    def add_ref(self, s):
        """Parse a string as a reference and add it to this fragment."""
        ref_tuple = self._ref_parser.parse(s)
        if not ref_tuple:
            return None
        self._insert_ref(ref_tuple)
        return ref_tuple

    def _parse_front_matter(self, fp):
        log = logging.getLogger(__name__)
        while 1:
            line = fp.readline()
            if not line:
                return
            line = line.strip()
            if line == FRONT_MATTER_DELIMITER:
                return
            if line.startswith("#"):
                # comment line
                continue

            # Strip "bullet points" so this can look more yaml-like
            if line.startswith("- "):
                line = line[2:].strip()
            log.debug("Front matter reference text: %s", line)
            result = self.add_ref(line)
            if result is None:
                raise RuntimeError(
                    "Could not parse line in front matter as reference:",
                    line)

    def _parse_io(self, fp):
        line = fp.readline()
        if line.strip() == FRONT_MATTER_DELIMITER:
            self._parse_front_matter(fp)
            line = fp.readline()
        while 1:
            if not line:
                break
            self.text += line
            line = fp.readline()
        self.text = self.text.strip()
        log = logging.getLogger(__name__)
        log.debug("Got fragment with prefix '%s', text starting with '%s'",
                  self.prefix, self.text[:20])

    def parse_file(self):
        """Open the file and parse content, and front matter if any.

        If io was provided at construction time, that is parsed instead.
        """
        if self.io is not None:
            self._parse_io(self.io)
            return
        with open(str(self.filename), 'r', encoding='utf-8') as fp:
            self._parse_io(fp)


class Section:
    """A section is a component/aspect of a project.

    Changes for a Section are (potentially) separated out in the news file.
    For example, sections might include "Drivers", "UI", etc.

    A section contains :class:`Fragment` objects. They are typically populated
    from a directory of files through a call to
    :func:`populate_from_directory()`. They are kept sorted.
    """

    def __init__(self,
                 name,
                 relative_directory=None,
                 sort_by_prefix=False):
        super().__init__()
        self.name = name
        self.relative_directory = relative_directory
        self.sort_by_prefix = sort_by_prefix
        self.fragments = []
        self._log = _LOG.getChild("Section." + name)

    def _sort_fragments(self):
        # Keep this list sorted
        self.fragments.sort()
        if self.sort_by_prefix:
            self._log.debug("Sorting by prefix here!")
            self.fragments.sort(key=attrgetter('prefix'))

    def add_fragment(self, fragment):
        """Add a fragment to this section.

        This does **not** call fragment.parse_file(). However,
        :func:`populate_from_directory()` is the usual place this gets
        called from, and it **does** call parse_file.
        """
        self.fragments.append(fragment)
        self._sort_fragments()
        self._log.debug("added: %s", fragment.filename)

    def populate_from_directory(self, directory, ref_parser):
        """Iterate through a directory, trying to parse each filename as a reference.

        Files that parse properly are assumed to be fragments,
        and a :class:`Fragment` object is instantiated for them.
        """
        if isinstance(directory, str):
            directory = Path(directory)
        for fragment_name in directory.iterdir():
            fragment_ref = ref_parser.parse(fragment_name.name)
            if not fragment_ref:
                # Actually not a fragment, skipping
                self._log.debug("Not actually a fragment: %s", fragment_name)
                continue
            fragment = Fragment(fragment_name, fragment_ref, ref_parser)
            fragment.parse_file()
            self.add_fragment(fragment)

        self._sort_fragments()

    @property
    def fragment_filenames(self):
        """Return a generator of filenames for all :class:`Fragment` objects
        added."""
        return (fragment.filename for fragment in self.fragments)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
