#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursegraphs.programming@arne.cl>

import os
from tempfile import NamedTemporaryFile

import pytest

import rstconverter as rstc
from rstconverter.dis.distree import DisRSTTree
from rstconverter.rs3 import RS3FileWriter, RSTTree

"""
Basic tests for the *.dis format for Rhetorical Structure Theory.

DisRSTTree parses a *.dis file into a parented tree (new, recommended, format
can be exported to *.rs3).
"""


def test_read_dis1_tree(fixtures_input_dir):
    input_tree = rstc.read_distree(os.path.join(fixtures_input_dir, 'rst-example1.dis'))
    assert isinstance(input_tree, DisRSTTree)

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert input_tree.tree == produced_output_tree.tree


def test_read_dis2_tree(fixtures_input_dir):
    input_tree = rstc.read_distree(os.path.join(fixtures_input_dir, 'rst-example2.dis'))
    assert isinstance(input_tree, DisRSTTree)

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert input_tree.tree == produced_output_tree.tree
