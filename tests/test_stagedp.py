#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursegraphs.programming@arne.cl>

import os
from tempfile import NamedTemporaryFile

import pytest

import rstconverter as rstc
from rstconverter.stagedp import StageDPRSTTree
from rstconverter.rs3 import RS3FileWriter, RSTTree

"""
Basic tests for the *.stagedp format for Rhetorical Structure Theory.
"""


def test_read_stagedp_one_edu(fixtures_input_dir):
    """the converter must not crash if the input only consists of one EDU."""
    input_tree = rstc.read_stagedp(os.path.join(fixtures_input_dir, 'one-edu.stagedp'))
    assert isinstance(input_tree, StageDPRSTTree)

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert input_tree.tree == produced_output_tree.tree


def test_read_stagedp_short(fixtures_input_dir):
    input_tree = rstc.read_stagedp(os.path.join(fixtures_input_dir, 'short.stagedp'))
    assert isinstance(input_tree, StageDPRSTTree)

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert input_tree.tree == produced_output_tree.tree



def test_read_stagedp_long(fixtures_input_dir):
    input_tree = rstc.read_stagedp(os.path.join(fixtures_input_dir, 'long.stagedp'))
    assert isinstance(input_tree, StageDPRSTTree)

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert input_tree.tree == produced_output_tree.tree


