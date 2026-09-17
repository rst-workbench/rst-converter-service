#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <rst-converter-service.programming@arne.cl>

"""Tests for the uniform contract of the low-level writers.

Every writer takes an optional output target (a path or a writable text
stream) and always returns the rendered string. If a target is given, the
string is also written to it. ``None`` means "return the string without
writing anywhere".
"""

import io

import pytest

import rstconverter as rstc


INPUT = 'tests/fixtures/input/short.rs3'

WRITERS = {
    'dis': rstc.write_dis,
    'rs3': rstc.write_rs3,
    'rstlatex': rstc.write_rstlatex,
    'svg': rstc.write_svgtree,
}


@pytest.fixture
def dgtree():
    return rstc.read_rs3tree(INPUT).tree


@pytest.mark.parametrize('writer', WRITERS.values(), ids=list(WRITERS))
def test_writer_returns_rendered_string(writer, dgtree):
    """Without an output target, the writer returns the rendered string."""
    result = writer(dgtree)

    assert isinstance(result, str)
    assert result != ''


@pytest.mark.parametrize('writer', WRITERS.values(), ids=list(WRITERS))
def test_writer_writes_to_path_and_returns_string(writer, dgtree, tmp_path):
    """With a path target, the writer writes the file and returns the string."""
    output_file = tmp_path / 'output.txt'

    result = writer(dgtree, str(output_file))

    assert isinstance(result, str)
    assert output_file.read_text() == result


@pytest.mark.parametrize('writer', WRITERS.values(), ids=list(WRITERS))
def test_writer_writes_to_stream_and_returns_string(writer, dgtree):
    """With a stream target, the writer writes the stream and returns the string."""
    buffer = io.StringIO()

    result = writer(dgtree, buffer)

    assert isinstance(result, str)
    assert buffer.getvalue() == result


@pytest.mark.parametrize('writer', WRITERS.values(), ids=list(WRITERS))
def test_writer_result_is_target_independent(writer, dgtree, tmp_path):
    """The returned string does not depend on the output target."""
    output_file = tmp_path / 'output.txt'
    buffer = io.StringIO()

    from_none = writer(dgtree)
    from_path = writer(dgtree, str(output_file))
    from_stream = writer(dgtree, buffer)

    assert from_none == from_path == from_stream == buffer.getvalue()
