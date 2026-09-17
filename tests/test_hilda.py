#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursegraphs.programming@arne.cl>

import os
from tempfile import NamedTemporaryFile

import pytest

import rstconverter as rstc
from rstconverter.hilda import HILDARSTTree
from rstconverter.rs3 import RS3FileWriter, RSTTree

"""
Basic tests for the *.hilda format for Rhetorical Structure Theory.
"""


def test_read_hilda1(fixtures_input_dir):
    input_tree = rstc.read_hilda(os.path.join(fixtures_input_dir, 'short.hilda'))
    assert isinstance(input_tree, HILDARSTTree)

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert input_tree.tree == produced_output_tree.tree


def test_read_hilda2(fixtures_input_dir):
    input_tree = rstc.read_hilda(os.path.join(fixtures_input_dir, 'long.hilda'))
    assert isinstance(input_tree, HILDARSTTree)

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert input_tree.tree == produced_output_tree.tree


def deep_hilda_str(depth):
    """Generate a right-branching chain of HILDA ParseTree expressions,
    as emitted by the Feng/Hirst parser for long documents.

    A nesting depth of 300 exceeds CPython's limit of ~200 nested
    parentheses in a single expression, which breaks eval()-based parsing,
    while staying below the recursion limits of the downstream conversion
    steps.
    """
    tree_str = "'leaf edu'"
    for i in range(depth):
        tree_str = "ParseTree('Joint[N][N]', [{}, 'edu {}'])".format(tree_str, i)
    return tree_str


def test_read_hilda_deeply_nested():
    depth = 300
    with NamedTemporaryFile('w', suffix='.hilda') as input_tempfile:
        input_tempfile.write(deep_hilda_str(depth))
        input_tempfile.flush()

        input_tree = rstc.read_hilda(input_tempfile.name)
        assert isinstance(input_tree, HILDARSTTree)
        assert len(input_tree.tree.leaves()) == depth + 1

        output_tempfile = NamedTemporaryFile()
        RS3FileWriter(input_tree, output_filepath=output_tempfile.name)
        produced_output_tree = RSTTree(output_tempfile.name)

        assert input_tree.tree == produced_output_tree.tree


def test_hildastr2hildatree_malformed_input():
    malformed_input = "ParseTree('Contrast[N][S]', ['an edu'"

    with pytest.raises(ValueError):
        HILDARSTTree.hildastr2hildatree(malformed_input)

