#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursegraphs.programming@arne.cl>

import os
from tempfile import NamedTemporaryFile

import pytest

import rstconverter as rstc
from rstconverter.tree import t

"""
Basic tests for parsing DPLP's output format for Rhetorical Structure Theory.
"""


def test_read_dplp_short(fixtures_input_dir):
    input_file = os.path.join(fixtures_input_dir, 'short.dplp')
    input_tree = rstc.read_dplp(input_file)

    tempfile = NamedTemporaryFile()
    rstc.write_rs3(input_tree, tempfile.name)
    produced_output_tree = rstc.read_rs3tree(tempfile.name)

    assert input_tree.tree == produced_output_tree.tree


def test_read_dplp_one_edu(fixtures_input_dir):
    input_file = os.path.join(fixtures_input_dir, 'one-edu.dplp')
    input_tree = rstc.read_dplp(input_file)

    tempfile = NamedTemporaryFile()
    rstc.write_rs3(input_tree, tempfile.name)
    produced_output_tree = rstc.read_rs3tree(tempfile.name)

    assert input_tree.tree == produced_output_tree.tree == t('N', ['good food .'])


def test_read_dplp_too_long(fixtures_input_dir):
    input_file = os.path.join(fixtures_input_dir, 'long.dplp')
    input_tree = rstc.read_dplp(input_file)

    tempfile = NamedTemporaryFile()
    rstc.write_rs3(input_tree, tempfile.name)
    produced_output_tree = rstc.read_rs3tree(tempfile.name)

    assert input_tree.tree == produced_output_tree.tree


def deep_dplp_str(depth):
    """Generate a .dplp file whose parse tree is a right-branching chain,
    as emitted by the DPLP parser for long documents.

    A nesting depth of 300 exceeds CPython's limit of ~200 nested
    parentheses in a single expression, which breaks eval()-based parsing,
    while staying below the recursion limits of the downstream conversion
    steps.
    """
    merge_lines = [
        "0\t{edu_id}\ttok{edu_id}\ttok\tVBD\troot\t0\tO\t (ROOT\t{edu_id}".format(edu_id=i + 1)
        for i in range(depth + 1)]
    tree_str = "ParentedTree('EDU', ['1'])"
    for i in range(1, depth + 1):
        tree_str = "ParentedTree('NS-elaboration', [{}, ParentedTree('EDU', ['{}'])])".format(
            tree_str, i + 1)
    return "\n".join(merge_lines) + "\n\n" + tree_str + "\n"


def test_read_dplp_deeply_nested():
    depth = 300
    with NamedTemporaryFile('w', suffix='.dplp') as input_tempfile:
        input_tempfile.write(deep_dplp_str(depth))
        input_tempfile.flush()

        input_tree = rstc.read_dplp(input_tempfile.name)

        output_tempfile = NamedTemporaryFile()
        rstc.write_rs3(input_tree, output_tempfile.name)
        produced_output_tree = rstc.read_rs3tree(output_tempfile.name)

        assert input_tree.tree == produced_output_tree.tree
