#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursegraphs.programming@arne.cl>

"""Basic tests for the ``rs3`` module"""

import logging
import os
from tempfile import NamedTemporaryFile

import pytest

import rstconverter as rstc
from rstconverter.rs3 import RS3FileWriter, RSTTree
from rstconverter.tree import DGParentedTree, t


RS3TREE_DIR = 'tests/fixtures/input/rs3tree'


def example2tree(rs3tree_example_filename, rs3tree_dir=RS3TREE_DIR, debug=False):
    """Given the filename of an rs3 file and its directory, return an RSTTree instance of it."""
    filepath = os.path.join(rs3tree_dir, rs3tree_example_filename)
    return RSTTree(filepath, debug=debug)


def test_rs3filewriter_emptytree():
    """An empty DGParentedTree is converted into an empty RS3 file and back."""
    input_tree = t("", [])
    expected_output_tree = example2tree("empty.rs3")

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert produced_output_tree.edu_strings == produced_output_tree.tree.leaves() == []
    assert input_tree == expected_output_tree.tree == produced_output_tree.tree


def test_rs3filewriter_onesegmenttree():
    """A DGParentedTree with only one segment is correctly converted into an RS3 file and back."""
    input_tree = t("N", ["foo"])
    expected_output_tree = example2tree('only-one-segment.rs3')

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert produced_output_tree.edu_strings == produced_output_tree.tree.leaves() == ['foo']
    assert input_tree == expected_output_tree.tree == produced_output_tree.tree


def test_rs3filewriter_onesegmenttree_umlauts():
    """A DGParentedTree with only one segment with umlauts is correctly
    converted into an RS3 file and back.
    """
    edu_string = "Über sein östliches Äußeres"
    input_tree = t("N", [edu_string])
    expected_output_tree = example2tree('only-one-segment-with-umlauts.rs3')

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert expected_output_tree.edu_strings == \
        produced_output_tree.edu_strings == \
        produced_output_tree.tree.leaves() == [edu_string]
    assert input_tree == expected_output_tree.tree == produced_output_tree.tree



def test_rs3filewriter_nucsat():
    """A DGParentedTree with one nuc-sat relation is correctly converted into an RS3 file and back."""
    input_tree = t("circumstance", [
        ("S", ["foo"]),
        ("N", ["bar"])])
    expected_output_tree = example2tree("foo-bar-circ-foo-to-bar.rs3")

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert produced_output_tree.edu_strings == produced_output_tree.tree.leaves() == ['foo', 'bar']
    assert input_tree == expected_output_tree.tree == produced_output_tree.tree

    input_tree = t("circumstance", [
        ("N", ["foo"]),
        ("S", ["bar"])])
    expected_output_tree = example2tree("foo-bar-circ-bar-to-foo.rs3")

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert produced_output_tree.edu_strings == produced_output_tree.tree.leaves() == ['foo', 'bar']
    assert input_tree == expected_output_tree.tree == produced_output_tree.tree


def test_rs3filewriter_nested():
    """A DGParentedTree with a multinuc relation nested in a nuc-sat relation
    is correctly converted into an RS3 file and back."""
    input_tree = t('elaboration', [
        ('N', ['eins']),
        ('S', [
            ('joint', [
                ('N', ['zwei']),
                ('N', ['drei'])])])])
    expected_output_tree = example2tree('eins-zwei-drei-(elab-eins-from-(joint-zwei-and-drei).rs3')

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert produced_output_tree.edu_strings == produced_output_tree.tree.leaves() == ['eins', 'zwei', 'drei']
    assert input_tree == expected_output_tree.tree == produced_output_tree.tree


def test_rs3filewriter_pcc_10575():
    """PCC rs3 file 10575 can be converted rs3 -> dgtree -> rs3' -> dgtree',
    without information loss between dgtree and dgtree'.
    """
    input_tree = t('interpretation', [
        ('N', [
            ('circumstance', [
                ('S', ['eins']),
                ('N', [
                    ('contrast', [
                        ('N', ['zwei']),
                        ('N', [
                            ('cause', [
                                ('N', ['drei']),
                                ('S', ['vier'])])])])])])]),
        ('S', ['fuenf'])])
    expected_output_tree = example2tree('maz-10575-excerpt.rs3')

    tempfile = NamedTemporaryFile()
    RS3FileWriter(input_tree, output_filepath=tempfile.name)
    produced_output_tree = RSTTree(tempfile.name)

    assert produced_output_tree.edu_strings == produced_output_tree.tree.leaves() == ['eins', 'zwei', 'drei', 'vier', 'fuenf']
    assert input_tree == expected_output_tree.tree == produced_output_tree.tree


# ~ @pytest.marker.xfail
# ~ def test_rs3filewriter_complete_pcc_stats():
    # ~ """All *.rs3 files can be parsed into a DGParentedTree (T1), converted back
    # ~ into *.rs3 files and parsed back into a DGParentedTree (T2), with T1 == T2.
    # ~ """
    # ~ okay = 0.0
    # ~ fail = 0.0

    # ~ for i, rfile in enumerate(dg.corpora.pcc.get_files_by_layer('rst')):
        # ~ try:
            # ~ # rs3 -> dgtree
            # ~ expected_output_tree = RSTTree(rfile)

            # ~ tempfile = NamedTemporaryFile()
            # ~ # dgtree -> rs3'
            # ~ RS3FileWriter(expected_output_tree, output_filepath=tempfile.name, debug=False)
            # ~ # rs3' -> dgtree'
            # ~ produced_output_tree = RSTTree(tempfile.name)

            # ~ assert expected_output_tree.edu_strings == expected_output_tree.tree.leaves() \
                # ~ == produced_output_tree.edu_strings == produced_output_tree.tree.leaves()
            # ~ assert expected_output_tree.tree == produced_output_tree.tree
            # ~ okay += 1

        # ~ except Exception as e:
            # ~ logging.log(logging.WARN,
                    # ~ "File '{0}' can't be loop-converted: {1}".format(
                        # ~ os.path.basename(rfile), e))
            # ~ fail += 1

    # ~ success_rate = okay / (okay+fail) * 100
    # ~ assert success_rate == 100, \
        # ~ "{0}% of PCC files could be loop-converted ({1} of {2})".format(success_rate, okay, okay+fail)
