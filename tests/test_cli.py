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


def run_cli_expecting_exit(monkeypatch, *args):
    """Run the CLI in-process, expecting it to exit via argparse."""
    fake_stdout = io.StringIO()
    fake_stderr = io.StringIO()
    monkeypatch.setattr(sys, 'argv', ['rst-converter'] + list(args))
    monkeypatch.setattr(sys, 'stdout', fake_stdout)
    monkeypatch.setattr(sys, 'stderr', fake_stderr)

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    return exc_info.value.code, fake_stdout.getvalue(), fake_stderr.getvalue()


def test_cli_help_lists_all_formats(monkeypatch):
    """--help lists all supported input and output formats."""
    exit_code, stdout, stderr = run_cli_expecting_exit(monkeypatch, '--help')

    assert exit_code == 0
    for input_format in cli.READ_FUNCTIONS:
        assert input_format in stdout
    for output_format in cli.WRITE_FUNCTIONS:
        assert output_format in stdout


def test_cli_missing_output_format_lists_formats(monkeypatch):
    """Omitting the output format reports the available output formats."""
    exit_code, stdout, stderr = run_cli_expecting_exit(
        monkeypatch, RS3_INPUT, 'rs3')

    assert exit_code != 0
    for output_format in cli.WRITE_FUNCTIONS:
        assert output_format in stderr


def test_cli_invalid_output_format_lists_formats(monkeypatch):
    """An unknown output format is rejected with the available formats."""
    exit_code, stdout, stderr = run_cli_expecting_exit(
        monkeypatch, RS3_INPUT, 'rs3', 'nope')

    assert exit_code != 0
    for output_format in cli.WRITE_FUNCTIONS:
        assert output_format in stderr


def test_cli_invalid_input_format_lists_formats(monkeypatch):
    """An unknown input format is rejected with the available formats."""
    exit_code, stdout, stderr = run_cli_expecting_exit(
        monkeypatch, RS3_INPUT, 'nope', 'dis')

    assert exit_code != 0
    for input_format in cli.READ_FUNCTIONS:
        assert input_format in stderr