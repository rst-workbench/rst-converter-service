#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursegraphs.programming@arne.cl>

"""
These Tests aim to show that RST trees remain unchanged, even after reconversion.
"""

import glob
import os
from tempfile import mkdtemp

import pytest

import rstconverter as rstc


PCC_RST_DIR = 'tests/fixtures/input/pcc/rst'


def test_rs3_dis_pcc_reconvert(rs3_dir=PCC_RST_DIR):
    """rs3->tree->dis->tree->rs3->tree"""
    temp_dir = mkdtemp()
    for rs3_file in glob.glob(os.path.join(rs3_dir, '*.rs3')):
        # rs3 -> tree
        rs3_fname = os.path.basename(rs3_file)
        rst_tree1 = rstc.read_rs3tree(rs3_file)

        # tree -> dis
        dis_fname = os.path.join(temp_dir, rs3_fname + '.dis')
        rstc.write_dis(rst_tree1, dis_fname)

        # dis -> tree'
        rst_tree2 = rstc.read_distree(dis_fname)

        # tree' -> rs3'
        rs3_fname_reconverted = os.path.join(temp_dir, rs3_fname + '_reconverted.rs3')
        rstc.write_rs3(rst_tree2, rs3_fname_reconverted)

        # rs3' -> tree''
        rst_tree3 = rstc.read_rs3tree(rs3_fname_reconverted)

        assert rst_tree1.tree.pformat() == rst_tree2.tree.pformat() == rst_tree3.tree.pformat()
