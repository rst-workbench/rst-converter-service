#!/usr/bin/env python
# coding: utf-8
# Author: Arne Neumann <discoursegraphs.programming@arne.cl>

from tempfile import NamedTemporaryFile

from lxml import etree

from rstconverter.tree import (debug_root_label,
    DGParentedTree, get_child_nodes, horizontal_positions, node2bracket,
    sorted_bfs_edges, sorted_bfs_successors, t, tree2bracket)
import rstconverter as rstc



EXPECTED_SVG_TREE = """<?xml version="1.0" encoding="utf-8" ?>
<svg baseProfile="full" height="72px" preserveAspectRatio="xMidYMid meet" style="font-family: times, serif; font-weight:normal; font-style: normal; font-size: 16px;" version="1.1" viewBox="0,0,80.0,72.0" width="80px" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs /><svg width="100%" x="0" y="0em"><defs /><text text-anchor="middle" x="50%" y="1em">foo</text></svg><svg width="50%" x="0%" y="3em"><defs /><svg width="100%" x="0" y="0em"><defs /><text text-anchor="middle" x="50%" y="1em">bar</text></svg></svg><line stroke="black" x1="50%" x2="25%" y1="1.2em" y2="3em" /><svg width="50%" x="50%" y="3em"><defs /><svg width="100%" x="0" y="0em"><defs /><text text-anchor="middle" x="50%" y="1em">baz</text></svg></svg><line stroke="black" x1="50%" x2="75%" y1="1.2em" y2="3em" /></svg>"""


def test_t():
    assert t("", []) == DGParentedTree("", [])
    assert t("") == DGParentedTree("", [])

    assert t("foo", []) == DGParentedTree("foo", [])
    assert t("foo") == DGParentedTree("foo", [])

    assert t("foo", ["bar"]) == DGParentedTree("foo", ["bar"])
    assert t("foo", ["bar", "baz"]) == DGParentedTree("foo", ["bar", "baz"])


def test_debug_root_label():
    label = 'Foo'
    node_id = '21'

    assert debug_root_label(label, debug=False, root_id=None) == label
    assert debug_root_label(label, debug=False, root_id=node_id) == label
    assert debug_root_label(label, debug=True, root_id=None) == label
    assert debug_root_label(label, debug=True, root_id=node_id) == "Foo (21)"


def test_write_svgtree():
    """A ParentedTree can be converted into an SVG image using svgling."""
    tree = DGParentedTree("foo", ["bar", "baz"])

    # write SVG to file
    temp_file = NamedTemporaryFile()
    temp_file.close()    
    rstc.write_svgtree(tree, temp_file.name)
    with open(temp_file.name, 'r') as svg_file:
        assert EXPECTED_SVG_TREE == svg_file.read()

    # return SVG as string
    assert EXPECTED_SVG_TREE == rstc.write_svgtree(tree)
