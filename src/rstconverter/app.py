#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Arne Neumann <nlpbox.programming@arne.cl>

"""This module contains a REST API for converting between different
RST (Rhetorical Structure Theory) formats.
"""

import base64
import io
import tempfile
import traceback
import warnings
from pathlib2 import Path

from flask import jsonify, Flask, request, send_file
from flask_restx import Resource, Api
from nltk.tree import TreePrettyPrinter
import werkzeug

import rstconverter as rstc

app = Flask(__name__)  # create a Flask app
api = Api(app)  # create a flask-restx API


def write_prettyprinted_nltktree(rst_basetree, output_file):
    """write a plain text ASCII-style representation of an RST tree to a file."""
    with rstc.tree.output_stream(output_file) as outfile:
        outfile.write(TreePrettyPrinter(rst_basetree.tree).text())

def write_svgtree(rst_basetree, output_file):
    """write an SVG image of the nltk.tree representation of an RST tree to a file."""
    wrapped_tree = rstc.tree.word_wrap_tree(rst_basetree.tree, width=20)
    rstc.tree.write_svgtree(wrapped_tree, output_file)

def write_nltktree_svg_base64(rst_basetree, output_file):
    """write a base64 representation of a SVG image
    of the nltk.tree representation of an RST tree to a file.
    """
    wrapped_tree = rstc.tree.word_wrap_tree(rst_basetree.tree, width=20)
    svg_string = rstc.tree.write_svgtree(wrapped_tree)
    base64_string = base64.b64encode(svg_string.encode()).decode('ascii')
    with rstc.tree.output_stream(output_file) as outfile:
        outfile.write(base64_string)



READ_FUNCTIONS = {
    'codra': rstc.read_codra,
    'dis': rstc.read_distree,
    'dplp': rstc.read_dplp,
    'hilda': rstc.read_hilda, # also used by Feng/Hirst (2014)
    'hs2015': rstc.read_hs2015tree,  # Heilman/Sagae (2015)
    'rs3': rstc.read_rs3tree,
    'stagedp': rstc.read_stagedp
}

WRITE_FUNCTIONS = {
    'dis': rstc.write_dis,
    'rs3': rstc.write_rs3,
    'rstlatex': rstc.write_rstlatex,
    'tree.prettyprint': write_prettyprinted_nltktree,
    'svg': write_svgtree,
    'svg-base64': write_nltktree_svg_base64
}

# Deprecated output format names (old -> canonical). They still work, but
# emit a deprecation warning and will be removed in a future release.
DEPRECATED_WRITE_ALIASES = {
    'svgtree': 'svg',
    'svgtree-base64': 'svg-base64',
}


def resolve_output_format(output_format):
    """Returns the canonical output format for the given output format name.

    If the name is a deprecated alias of a canonical format, a deprecation
    warning is emitted (both as a Python warning and in the application log).
    """
    canonical_format = DEPRECATED_WRITE_ALIASES.get(output_format)
    if canonical_format is not None:
        message = ("Output format '{old}' is deprecated, "
                   "use '{new}' instead.").format(old=output_format,
                                                  new=canonical_format)
        warnings.warn(message, DeprecationWarning, stacklevel=2)
        app.logger.warning(message)
        return canonical_format, True
    return output_format, False


@api.route('/input-formats')
class InputFormats(Resource):
    def get(self):
        """Returns a list of available input formats."""
        # Note: we can't use 'urml' as an input format, because it is
        # based on graphs, while all other formats use trees.
        return sorted(READ_FUNCTIONS.keys())


@api.route('/output-formats')
class OutputFormats(Resource):
    def get(self):
        """Returns a list of available output formats."""
        return sorted(WRITE_FUNCTIONS.keys())


@api.route('/convert/<string:input_format>/<string:output_format>')
class FormatConverter(Resource):
    def post(self, input_format, output_format):
        """Convert from one RST format to another.

        Usage example:

            curl -XPOST "http://localhost:5000/convert/rs3/dis" -F input=@source.rs3
        """
        input_file = get_input_file(request)
        if input_file is None:
            res = jsonify(
                error=("Please upload a file using the key "
                       "'input' or the form field 'input'. "
                       "Used file keys: {}. Used form fields: {}").format(list(request.files.keys()), list(request.form.keys())))
            return cors_response(res, 500)

        input_basename = Path(input_file.filename).stem

        with tempfile.NamedTemporaryFile() as temp_inputfile:
            input_file.save(temp_inputfile.name)

            if input_format not in READ_FUNCTIONS:
                res = jsonify(error="Unknown input format: {}".format(input_format))
                return cors_response(res, 400)

            read_function = READ_FUNCTIONS[input_format]

            try:
                tree = read_function(temp_inputfile.name)
            except Exception as err:
                error_msg = "{0} can't handle input file '{1}'. Got: {2}".format(
                    read_function, input_file.filename, err)
                res = jsonify(error=error_msg, traceback=traceback.format_exc())
                return cors_response(res, 500)

        with tempfile.NamedTemporaryFile() as temp_outputfile:
            canonical_format, deprecated = resolve_output_format(output_format)
            if canonical_format not in WRITE_FUNCTIONS:
                res = jsonify(error="Unknown output format: {}".format(output_format))
                return cors_response(res, 400)

            write_function = WRITE_FUNCTIONS[canonical_format]

            try:
                write_function(tree, output_file=temp_outputfile.name)
            except Exception as err:
                error_msg = ("{writer} can't convert ParentedTree to {output_format}. "
                            "Input file '{input_file}'. Got: {error}").format(
                    writer=write_function, output_format=canonical_format,
                    input_file=input_file.filename, error=err)
                res = jsonify(error=error_msg, traceback=traceback.format_exc())
                return cors_response(res, 500)

            output_filename = "{0}.{1}".format(input_basename, canonical_format)
            res = send_file(temp_outputfile.name, as_attachment=True,
                            download_name=output_filename)
            if deprecated:
                res.headers['Deprecation'] = 'true'
        return cors_response(res)


def get_input_file(request):
    """Returns the input file from the POST request (no matter if it was sent as
    a file named 'input' or a form field named 'input').
    Returns None if the POST request does not have an 'input' file.
    """
    if 'input' in request.files:
        return request.files['input']
    elif 'input' in request.form:
        input_string = request.form['input']
        stringio_file = io.StringIO(input_string)
        return werkzeug.FileStorage(stringio_file, 'input.ext')


def cors_response(response, status=200):
    """Returns the given response with CORS='*' and the given status code."""
    response.status_code = status
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def main():
    app.run(debug=False, host='0.0.0.0')

if __name__ == '__main__':
    main()
