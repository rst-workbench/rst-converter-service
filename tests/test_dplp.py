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
