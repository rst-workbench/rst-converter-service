#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <rst-converter-service.programming@arne.cl>

"""Tests for the command line interface (rst-converter)."""

import io
import os
import sys

import pytest

import rstconverter as rstc
import rstconverter.cli as cli


INPUT_DIR = 'tests/fixtures/input'
OUTPUT_DIR = 'tests/fixtures/output'

RS3_INPUT = os.path.join(INPUT_DIR, 'short.rs3')

OUTPUT_FORMATS = sorted(cli.WRITE_FUNCTIONS.keys())


def run_cli(monkeypatch, *args):
    """Run the CLI in-process and return the text it wrote to stdout."""
    fake_stdout = io.StringIO()
    monkeypatch.setattr(sys, 'argv', ['rst-converter'] + list(args))
    monkeypatch.setattr(sys, 'stdout', fake_stdout)
    cli.main()
    return fake_stdout.getvalue()


@pytest.mark.parametrize('output_format', OUTPUT_FORMATS)
def test_cli_writes_to_stdout(monkeypatch, output_format):
    """If no output file is given, the CLI writes the result to stdout."""
    stdout = run_cli(monkeypatch, RS3_INPUT, 'rs3', output_format)

    assert stdout != ''
    assert not os.path.exists('<stdout>')


def test_cli_writes_to_file(monkeypatch, tmp_path):
    """If an output file is given, the CLI writes the result to that file."""
    output_file = tmp_path / 'short.rs3.dis'
    stdout = run_cli(monkeypatch, RS3_INPUT, 'rs3', 'dis', str(output_file))

    assert stdout == ''
    with open(os.path.join(OUTPUT_DIR, 'short.rs3.dis')) as expected_file:
        assert output_file.read_text() == expected_file.read()


@pytest.mark.parametrize('output_format', OUTPUT_FORMATS)
def test_writer_accepts_file_like_object(output_format):
    """All writers can write to a file-like object instead of a path."""
    tree = rstc.read_rs3tree(RS3_INPUT)
    buffer = io.StringIO()

    cli.WRITE_FUNCTIONS[output_format](tree, output_file=buffer)

    assert buffer.getvalue() != ''