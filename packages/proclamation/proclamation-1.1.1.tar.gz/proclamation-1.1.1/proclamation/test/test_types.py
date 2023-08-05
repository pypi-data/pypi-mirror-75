#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd. and the Proclamation contributors
#
# SPDX-License-Identifier: Apache-2.0

import tempfile
from io import StringIO
from pathlib import Path

from ..types import Fragment, ReferenceParser, Section


def test_ref_parse():
    parser = ReferenceParser()
    assert(parser.parse("issue.54.md").item_type == "issue")
    assert(parser.parse("issue.54.md").number == 54)
    assert(parser.parse("issue.54.md").as_tuple() == ("issue", 54, ()))

    assert(parser.parse("issue.54").item_type == "issue")
    assert(parser.parse("issue.54").number == 54)
    assert(parser.parse("issue.54").as_tuple() == ("issue", 54, ()))

    assert(parser.parse("issue.54").as_tuple() ==
           parser.parse("issue.54.md").as_tuple())

    assert(parser.parse("issue.54.gh").as_tuple() == ("issue", 54, ("gh",)))
    assert(parser.parse("issue.54.gh").as_tuple() ==
           parser.parse("issue.54.gh.md").as_tuple())

    assert(parser.parse(".gitignore") is None)
    assert(parser.parse(".git-keep") is None)


def test_ref_parse_filename():
    parser = ReferenceParser()
    assert(parser.parse_filename("issue.54.md").item_type == "issue")
    assert(parser.parse_filename("issue.54.md").number == 54)
    assert(parser.parse_filename("issue.54.md").as_tuple() == ("issue", 54, ()))
    assert(parser.parse_filename("issue.54.gh.md").as_tuple()
           == ("issue", 54, ("gh",)))
    assert(parser.parse_filename("issue.54") is None)
    assert(parser.parse_filename(".gitignore") is None)
    assert(parser.parse_filename(".git-keep") is None)


FRAGMENT = """---
- issue.55
- mr.23
pr.25
issue.54
---
This is content.
"""


def test_fragment():
    fn = "issue.54.md"
    fragmentio = StringIO(FRAGMENT)
    fragment = Fragment(fn, io=fragmentio)
    assert(str(fragment.filename) == fn)
    assert(len(fragment.refs) == 1)
    fragment.parse_file()
    assert("content" in fragment.text)
    assert("---" not in fragment.text)

    # duplicates don't get added
    assert(len(fragment.refs) == 4)


FRAGMENT_ERROR = """---
- issue.55
- mr.23
pr.25
issue.54
err
---
This is content.
"""


def test_fragment_with_error():
    fn = "issue.54.md"
    fragmentio = StringIO(FRAGMENT_ERROR)
    fragment = Fragment(fn, io=fragmentio)
    try:
        fragment.parse_file()
    except RuntimeError as e:
        assert("Could not parse line" in str(e))
        return
    assert(False)  # We expect an error.


SIMPLE_FRAGMENT = """This is a simple fragment content.
"""


def test_simple_fragment():
    fn = "issue.54.md"
    fragmentio = StringIO(SIMPLE_FRAGMENT)
    fragment = Fragment(fn, io=fragmentio)
    assert(str(fragment.filename) == fn)
    assert(len(fragment.refs) == 1)
    fragment.parse_file()
    assert(len(fragment.refs) == 1)
    assert("content" in fragment.text)


FRAGMENT_WITH_COMMENTS = """---
# comment
- issue.55
- mr.23
   # comment
pr.25
# comment
---
This is content.
"""


def test_fragment_prefix_size_limit():
    fn = "issue.54.md"
    fragment_text = (
        "This is a really really long sample fragment. "
        "It has a colon because of a URL, but that's not a prefix. "
        "<https://gitlab.com/ryanpavlik/proclamation>"
    )
    fragmentio = StringIO(fragment_text)
    fragment = Fragment(fn, io=fragmentio)
    # Haven't parsed the text yet
    assert(fragment.prefix == '')
    fragment.parse_file()
    assert(fragment.prefix == 'This')


def test_fragment_with_comment():
    fn = "issue.54.md"
    fragmentio = StringIO(FRAGMENT_WITH_COMMENTS)
    fragment = Fragment(fn, io=fragmentio)
    assert(str(fragment.filename) == fn)
    assert(len(fragment.refs) == 1)
    fragment.parse_file()
    # skips comments
    assert(len(fragment.refs) == 4)
    assert("---" not in fragment.text)
    assert("comment" not in fragment.text)
    print(fragment.refs)


PREFIX_DATA = (
    ("mr.1544.md", "Document new thing"),
    ("mr.1729.md", "Make generation of event explicit"),
    ("mr.1731.md", "Document another new thing"),
)


def create_fragments(dirname):
    our_dir = Path(dirname)
    for fn, contents in PREFIX_DATA:
        with open(str(our_dir/fn), 'w') as fp:
            fp.write(contents)
            fp.write('\n')


def test_fragment_sorting_from_disk():
    with tempfile.TemporaryDirectory() as dirname:
        create_fragments(dirname)
        section = Section("MySection")
        section.populate_from_directory(dirname, ReferenceParser())
        assert(section.fragments[0].ref.as_tuple() == ("mr", 1544, ()))
        assert(section.fragments[1].ref.as_tuple() == ("mr", 1729, ()))
        assert(section.fragments[2].ref.as_tuple() == ("mr", 1731, ()))


def test_fragment_sorting():
    section = Section("MySection")

    frag_b = Fragment("issue.2.md")
    section.add_fragment(frag_b)
    assert(section.fragments[0] == frag_b)

    frag_a = Fragment("issue.1.md")
    section.add_fragment(frag_a)
    assert(section.fragments[0] == frag_a)
    assert(section.fragments[1] == frag_b)

    frag_c = Fragment("issue.2.2.md")
    section.add_fragment(frag_c)
    assert(section.fragments[0] == frag_a)
    assert(section.fragments[1] == frag_b)
    assert(section.fragments[2] == frag_c)


def test_fragment_sorting_prefix():
    section = Section("MySection", sort_by_prefix=True)

    frag_add = Fragment("issue.2.md")
    frag_add.text = "Add: abc"
    assert(frag_add.prefix == "Add")
    section.add_fragment(frag_add)
    assert(section.fragments[0] == frag_add)

    frag_fix = Fragment("issue.1.md")
    frag_fix.text = "Fix: abc"
    assert(frag_fix.prefix == "Fix")
    section.add_fragment(frag_fix)
    # this one starts with "Add"
    assert(section.fragments[0] == frag_add)
    # This one starts with "Fix"
    assert(section.fragments[1] == frag_fix)


def test_fragment_sorting_prefix2():
    section = Section("MySection", sort_by_prefix=True)

    frag_doc_1 = Fragment(PREFIX_DATA[0][0])
    frag_doc_1.text = PREFIX_DATA[0][1]
    assert(frag_doc_1.prefix == "Document")
    section.add_fragment(frag_doc_1)
    assert(section.fragments[0] == frag_doc_1)

    frag_make = Fragment(PREFIX_DATA[1][0])
    frag_make.text = PREFIX_DATA[1][1]
    assert(frag_make.prefix == "Make")
    section.add_fragment(frag_make)
    # this one starts with "Document"
    assert(section.fragments[0] == frag_doc_1)
    # This one starts with "Make"
    assert(section.fragments[1] == frag_make)

    frag_doc_2 = Fragment(PREFIX_DATA[2][0])
    frag_doc_2.text = PREFIX_DATA[2][1]
    assert(frag_doc_2.prefix == "Document")
    section.add_fragment(frag_doc_2)
    # these start with "Document"
    assert(section.fragments[0] == frag_doc_1)
    assert(section.fragments[1] == frag_doc_2)
    # This one starts with "Make"
    assert(section.fragments[2] == frag_make)


def test_fragment_sorting_prefix_from_disk():
    with tempfile.TemporaryDirectory() as dirname:
        create_fragments(dirname)
        section = Section("MySection", sort_by_prefix=True)
        section.populate_from_directory(dirname, ReferenceParser())

        # these start with "Document"
        assert(section.fragments[0].prefix == "Document")
        assert(section.fragments[0].ref.as_tuple() == ("mr", 1544, ()))
        assert(section.fragments[1].prefix == "Document")
        assert(section.fragments[1].ref.as_tuple() == ("mr", 1731, ()))
        # This one starts with "Make"
        assert(section.fragments[2].prefix == "Make")
        assert(section.fragments[2].ref.as_tuple() == ("mr", 1729, ()))
