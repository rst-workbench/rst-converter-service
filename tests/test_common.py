#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursegraphs.programming@arne.cl>

import pytest

from nltk.tree import Tree

from rstconverter.common import parse_bracketed_tree

"""
Unit tests for the iterative parser for bracketed parse tree expressions
(e.g. HILDA's ParseTree and DPLP's ParentedTree output format).
"""


def test_parse_simple_tree():
    tree = parse_bracketed_tree("ParseTree('Contrast[S][N]', ['a', 'b'])")

    assert isinstance(tree, Tree)
    assert tree.label() == 'Contrast[S][N]'
    assert tree.leaves() == ['a', 'b']


def test_parse_nested_tree():
    input_str = ("ParseTree('Elaboration[N][S]', "
                 "[ParseTree('Joint[N][N]', ['a', 'b']), 'c'])")
    tree = parse_bracketed_tree(input_str)

    assert tree.label() == 'Elaboration[N][S]'
    assert len(tree) == 2
    assert tree[0].label() == 'Joint[N][N]'
    assert tree[0].leaves() == ['a', 'b']
    assert tree[1] == 'c'


def test_parse_parented_tree():
    input_str = ("ParentedTree('NS-elaboration', "
                 "[ParentedTree('EDU', ['1']), ParentedTree('EDU', ['2'])])")
    tree = parse_bracketed_tree(input_str, 'ParentedTree')

    assert tree.label() == 'NS-elaboration'
    assert tree[0].label() == 'EDU'
    assert tree.leaves() == ['1', '2']


def test_parse_whitespace_tolerance():
    input_str = "ParseTree('Contrast[S][N]' ,\n  [ 'a' ,\n 'b' ] )\n"
    tree = parse_bracketed_tree(input_str)

    assert tree.leaves() == ['a', 'b']


def test_parse_empty_children():
    tree = parse_bracketed_tree("ParseTree('N', [])")

    assert isinstance(tree, Tree)
    assert len(tree) == 0


def test_parse_escaped_backslash_in_string():
    input_str = r"ParseTree('N', ['a \\ b'])"
    tree = parse_bracketed_tree(input_str)

    assert tree.leaves() == ['a \\ b']


def test_parse_unterminated_string_raises():
    with pytest.raises(ValueError):
        parse_bracketed_tree("ParseTree('N', ['abc")


def test_parse_unquoted_label_raises():
    with pytest.raises(ValueError):
        parse_bracketed_tree("ParseTree(unquoted, ['a'])")


def test_parse_missing_comma_raises():
    with pytest.raises(ValueError):
        parse_bracketed_tree("ParseTree('N' ['a'])")


def test_parse_stray_closing_bracket_raises():
    with pytest.raises(ValueError):
        parse_bracketed_tree("ParseTree('N', ['a'])]")


def test_parse_unclosed_children_list_raises():
    with pytest.raises(ValueError):
        parse_bracketed_tree("ParseTree('N', ['a', 'b'")


def test_parse_trailing_junk_raises():
    with pytest.raises(ValueError,
                       match="malformed parse tree input at position"):
        parse_bracketed_tree("ParseTree('N', ['a', 'b']) junk")


def test_parse_bare_leaf_raises():
    with pytest.raises(ValueError):
        parse_bracketed_tree("'just a leaf'")


def test_parse_multiple_top_level_trees_raises():
    input_str = ("ParseTree('A[N][N]', ['x', 'y']) "
                 "ParseTree('B[N][N]', ['p', 'q'])")

    with pytest.raises(ValueError):
        parse_bracketed_tree(input_str)
