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

