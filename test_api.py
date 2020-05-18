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


EXPECTED_RS3_DIS = u"(Root\n  (span 1 2)\n  (Satellite\n    (leaf 1)\n    (rel2par Contrast)\n    (text _!Although they did n't like it ,_!))\n  (Nucleus\n    (leaf 2)\n    (rel2par span)\n    (text _!they accepted the offer ._!)))"
EXPECTED_RS3_RSTLATEX = u"\\dirrel\n\t{Contrast}{\\rstsegment{Although they did n't like it ,}}\n\t{}{\\rstsegment{they accepted the offer .}}\n"
EXPECTED_HS2015_RS3 = EXPECTED_HILDA_RS3 = EXPECTED_CODRA_RS3 = u'<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<rst>\n  <header>\n    <relations>\n      <rel name="Contrast" type="rst"/>\n    </relations>\n  </header>\n  <body>\n    <segment id="3" parent="5" relname="Contrast">Although they did n\'t like it ,</segment>\n    <segment id="5" parent="1" relname="span">they accepted the offer .</segment>\n    <group id="1" type="span"/>\n  </body>\n</rst>\n'
EXPECTED_DIS_RS3 = u'<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<rst>\n  <header>\n    <relations>\n      <rel name="Same-Unit" type="multinuc"/>\n      <rel name="attribution" type="rst"/>\n      <rel name="consequence-n" type="rst"/>\n      <rel name="elaboration-additional" type="rst"/>\n      <rel name="elaboration-additional-e" type="rst"/>\n    </relations>\n  </header>\n  <body>\n    <segment id="7" parent="9" relname="attribution">blah blah blah</segment>\n    <segment id="11" parent="9" relname="span">blah blah blah</segment>\n    <segment id="13" parent="11" relname="consequence-n">blah blah blah</segment>\n    <segment id="15" parent="5" relname="elaboration-additional">blah blah blah</segment>\n    <segment id="21" parent="19" relname="span">blah blah blah</segment>\n    <segment id="23" parent="21" relname="elaboration-additional-e">blah blah blah</segment>\n    <segment id="25" parent="17" relname="Same-Unit">blah blah blah</segment>\n    <group id="1" type="span"/>\n    <group id="3" type="span" parent="1" relname="span"/>\n    <group id="5" type="span" parent="3" relname="span"/>\n    <group id="9" type="span" parent="5" relname="span"/>\n    <group id="17" type="multinuc" parent="3" relname="elaboration-additional"/>\n    <group id="19" type="span" parent="17" relname="Same-Unit"/>\n  </body>\n</rst>\n'
EXPECTED_DPLP_RS3 = u'<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<rst>\n  <header>\n    <relations>\n      <rel name="elaboration" type="rst"/>\n    </relations>\n  </header>\n  <body>\n    <segment id="3" parent="1" relname="span">Although they didn\'t like it,</segment>\n    <segment id="5" parent="3" relname="elaboration">they accepted the offer.</segment>\n    <group id="1" type="span"/>\n  </body>\n</rst>\n'
EXPECTED_RS3_SVGTREE = u'<?xml version="1.0" encoding="utf-8" ?>\n<svg baseProfile="full" height="136px" preserveAspectRatio="xMidYMid meet" style="font-family: times, serif; font-weight:normal; font-style: normal; font-size: 16px;" version="1.1" viewBox="0,0,304.0,136.0" width="304px" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs /><svg width="100%" x="0" y="0em"><defs /><text text-anchor="middle" x="50%" y="1em">Contrast</text></svg><svg width="50%" x="0%" y="3em"><defs /><svg width="100%" x="0" y="0em"><defs /><text text-anchor="middle" x="50%" y="1em">S</text></svg><svg width="100%" x="0%" y="3em"><defs /><svg width="100%" x="0" y="0em"><defs /><text text-anchor="middle" x="50%" y="1em">Although they did</text><text text-anchor="middle" x="50%" y="2em">n\'t like it ,</text></svg></svg><line stroke="black" x1="50%" x2="50%" y1="1.2em" y2="3em" /></svg><line stroke="black" x1="50%" x2="25%" y1="1.2em" y2="3em" /><svg width="50%" x="50%" y="3em"><defs /><svg width="100%" x="0" y="0em"><defs /><text text-anchor="middle" x="50%" y="1em">N</text></svg><svg width="100%" x="0%" y="3em"><defs /><svg width="100%" x="0" y="0em"><defs /><text text-anchor="middle" x="50%" y="1em">they accepted the</text><text text-anchor="middle" x="50%" y="2em">offer .</text></svg></svg><line stroke="black" x1="50%" x2="50%" y1="1.2em" y2="3em" /></svg><line stroke="black" x1="50%" x2="75%" y1="1.2em" y2="3em" /></svg>'


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
    assert res.content.decode('utf-8') == EXPECTED_CODRA_RS3

def test_convert_dis2rs3():
    """API converts file from dis to rs3 format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'rst-example1.dis')
    res = post_file(input_filepath, 'dis', 'rs3')
    assert res.content.decode('utf-8') == EXPECTED_DIS_RS3

def test_convert_dplp2rs3():
    """API converts file from DPLP to rs3 format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.dplp')
    res = post_file(input_filepath, 'dplp', 'rs3')
    assert res.content.decode('utf-8') == EXPECTED_DPLP_RS3

def test_convert_hilda2rs3():
    """API converts file from HILDA to rs3 format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.hilda')
    res = post_file(input_filepath, 'hilda', 'rs3')
    assert res.content.decode('utf-8') == EXPECTED_HILDA_RS3

def test_convert_hs2015tors3():
    """API converts file from Heilman/Sagae to rs3 format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.hs2015')
    res = post_file(input_filepath, 'hs2015', 'rs3')
    assert res.content.decode('utf-8') == EXPECTED_HS2015_RS3

def test_convert_rs3todis():
    """API converts file from rs3 to dis format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.rs3')
    res = post_file(input_filepath, 'rs3', 'dis')
    assert res.content.decode('utf-8') == EXPECTED_RS3_DIS

def test_convert_rs3torstlatex():
    """API converts file from rs3 to rstlatex format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.rs3')
    res = post_file(input_filepath, 'rs3', 'rstlatex')
    assert res.content.decode('utf-8') == EXPECTED_RS3_RSTLATEX

def test_convert_rs3tosvgtree():
    """API converts file from rs3 to svgtree format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.rs3')
    res = post_file(input_filepath, 'rs3', 'svgtree')
    assert res.content.decode('utf-8') == EXPECTED_RS3_SVGTREE

def test_convert_rs3tosvgtree_base64():
    """API converts file from rs3 to svgtree-base64 format"""
    input_filepath = os.path.join(dg.DATA_ROOT_DIR, 'short.rs3')
    res = post_file(input_filepath, 'rs3', 'svgtree-base64')
    svg_base64 = res.content.decode('utf-8')
    assert base64.b64decode(svg_base64) == EXPECTED_RS3_SVGTREE

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
