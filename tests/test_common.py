#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursegraphs.programming@arne.cl>

import pytest

from rstconverter.common import parse_bracketed_tree

"""
Unit tests for the iterative parser for bracketed parse tree expressions
(e.g. HILDA's ParseTree and DPLP's ParentedTree output format).
"""


def test_parse_bare_leaf_raises():
    with pytest.raises(ValueError):
        parse_bracketed_tree("'just a leaf'")


def test_parse_multiple_top_level_trees_raises():
    input_str = ("ParseTree('A[N][N]', ['x', 'y']) "
                 "ParseTree('B[N][N]', ['p', 'q'])")

    with pytest.raises(ValueError):
        parse_bracketed_tree(input_str)
