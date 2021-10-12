#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursegraphs.programming@arne.cl>

import os
from tempfile import NamedTemporaryFile

import pytest

import rstconverter as rstc
from rstconverter.heilman_sagae_2015 import HS2015RSTTree
from rstconverter.rs3 import RS3FileWriter, RSTTree

"""
Basic tests for the *.hs2015 (Heilman/Sagae 2015) format for Rhetorical Structure Theory.
"""


def test_read_hs2015a(fixtures_input_dir):
    input_tree = rstc.read_hs2015tree(os.path.join(fixtures_input_dir, 'short.hs2015'))
    assert isinstance(input_tree, HS2015RSTTree)

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert input_tree.tree == produced_output_tree.tree


def test_read_hs2015b(fixtures_input_dir):
    input_tree = rstc.read_hs2015tree(os.path.join(fixtures_input_dir, 'long.hs2015'))

    assert isinstance(input_tree, HS2015RSTTree)

    tempfile = NamedTemporaryFile()

    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert input_tree.tree == produced_output_tree.tree

