#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Arne Neumann <nlpbox.programming@arne.cl>

"""Tests for the REST API for converting between different RST file formats."""

from __future__ import print_function
import base64
import os
import pexpect
import pytest
import requests

import discoursegraphs as dg



def read_file(filepath):
    with open(filepath) as input_file:
        return input_file.read()


@pytest.fixture(scope="session", autouse=True)
def start_api():
    """Starts the REST API in the background."""
    print("starting API...")
    child = pexpect.spawn('python app.py')
    yield child.expect('(?i)Running on http://0.0.0.0:5000/') # provide the fixture value
    print("stopping API...")
    child.close()

def post_file(input_filepath, input_format, output_format):
    """Posts a file to the REST API and converts between the given formats."""
    with open(input_filepath) as input_file:
        input_text = input_file.read()
        url = 'http://localhost:5000/convert/{}/{}'.format(
            input_format, output_format)
        return requests.post(url, files={'input': input_text})

def test_convert_codra2rs3():
    """API converts file from codra to rs3 format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.codra')
    res = post_file(input_filepath, 'codra', 'rs3')
    assert res.content.decode('utf-8') == read_file('tests/fixtures/output/short.codra.rs3')

def test_convert_dis2rs3():
    """API converts file from dis to rs3 format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'rst-example1.dis')
    res = post_file(input_filepath, 'dis', 'rs3')
    assert res.content.decode('utf-8') == read_file('tests/fixtures/output/short.dis.rs3')

def test_convert_dplp2rs3():
    """API converts file from DPLP to rs3 format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.dplp')
    res = post_file(input_filepath, 'dplp', 'rs3')
    assert res.content.decode('utf-8') == read_file('tests/fixtures/output/short.dplp.rs3')

def test_convert_hilda2rs3():
    """API converts file from HILDA to rs3 format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.hilda')
    res = post_file(input_filepath, 'hilda', 'rs3')
    assert res.content.decode('utf-8') == read_file('tests/fixtures/output/short.hs2015.rs3')

def test_convert_hs2015tors3():
    """API converts file from Heilman/Sagae to rs3 format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.hs2015')
    res = post_file(input_filepath, 'hs2015', 'rs3')
    assert res.content.decode('utf-8') == read_file('tests/fixtures/output/short.hs2015.rs3')

def test_convert_stagedptors3():
    """API converts file from StageDP (Wang 2017) to rs3 format."""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.stagedp')
    res = post_file(input_filepath, 'stagedp', 'rs3')
    assert res.content.decode('utf-8') == read_file('tests/fixtures/output/short.stagedp.rs3')

def test_convert_rs3todis():
    """API converts file from rs3 to dis format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.rs3')
    res = post_file(input_filepath, 'rs3', 'dis')
    assert res.content.decode('utf-8') == read_file('tests/fixtures/output/short.rs3.dis')

def test_convert_rs3torstlatex():
    """API converts file from rs3 to rstlatex format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.rs3')
    res = post_file(input_filepath, 'rs3', 'rstlatex')
    assert res.content.decode('utf-8') == read_file('tests/fixtures/output/short.rs3.rstlatex')

def test_convert_rs3tosvgtree():
    """API converts file from rs3 to svgtree format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.rs3')
    res = post_file(input_filepath, 'rs3', 'svgtree')
    assert res.content.decode('utf-8') == read_file('tests/fixtures/output/short.rs3.svgtree')

def test_convert_rs3tosvgtree_base64():
    """API converts file from rs3 to svgtree-base64 format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.rs3')
    res = post_file(input_filepath, 'rs3', 'svgtree-base64')
    svg_base64 = res.content.decode('utf-8')
    assert base64.b64decode(svg_base64) == read_file('tests/fixtures/output/short.rs3.svgtree')

def test_missing_parameters():
    """Calling the API with missing parameters results in an error"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.rs3')

    with open(input_filepath) as input_file:
        input_text = input_file.read()

        # no format parameters
        url = 'http://localhost:5000/convert/'
        res = requests.post(url, files={'input': input_text})
        assert res.status_code != 200

        # no output format
        url = 'http://localhost:5000/convert/{}'.format('rs3')
        res = requests.post(url, files={'input': input_text})
        assert res.status_code != 200

        # no input file
        url = 'http://localhost:5000/convert/{}/{}'.format('rs3', 'dis')
        res = requests.post(url)
        assert res.status_code != 200

        # no / wrong 'input' file parameter
        url = 'http://localhost:5000/convert/{}/{}'.format('rs3', 'dis')
        res = requests.post(url, files={'wrong_param': input_text})
        assert res.status_code != 200

def test_unknown_formats():
    """Calling the API with unknown formats results in an error"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.rs3')

    # wrong input format
    res = post_file(input_filepath, 'wrong_format', 'dis')
    assert res.status_code != 200

    # wrong output format
    res = post_file(input_filepath, 'rs3', 'wrong_format')
    assert res.status_code != 200

def test_convert_one_edu_dplp2tree():
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'one-edu.dplp')
    res = post_file(input_filepath, 'dplp', 'tree.prettyprint')
    assert res.content.decode('utf-8') == read_file('tests/fixtures/output/one-edu.dplp.tree.prettyprint')
