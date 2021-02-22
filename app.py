#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Author: Arne Neumann <nlpbox.programming@arne.cl>

"""This module contains a REST API for converting between different
RST (Rhetorical Structure Theory) formats.
"""

import base64
import codecs
import io
import tempfile
import traceback
from pathlib2 import Path

from flask import jsonify, Flask, request, send_file
from flask_restplus import Resource, Api
from nltk.treeprettyprinter import TreePrettyPrinter
import werkzeug

import discoursegraphs as dg

app = Flask(__name__)  # create a Flask app
api = Api(app)  # create a Flask-RESTPlus API


def write_prettyprinted_nltktree(rst_basetree, output_file):
    """write a plain text ASCII-style representation of an RST tree to a file."""
    with codecs.open(output_file, 'w', 'utf-8') as outfile:
        outfile.write(TreePrettyPrinter(rst_basetree.tree).text())

def write_svgtree(rst_basetree, output_file):
    """write an SVG image of the nltk.tree representation of an RST tree to a file."""
    wrapped_tree = dg.readwrite.tree.word_wrap_tree(rst_basetree.tree, width=20)
    dg.readwrite.tree.write_svgtree(wrapped_tree, output_file)

def write_nltktree_svg_base64(rst_basetree, output_file):
    """write a base64 representation of a SVG image
    of the nltk.tree representation of an RST tree to a file.
    """
    with open(output_file, 'wb') as outfile:
        wrapped_tree = dg.readwrite.tree.word_wrap_tree(rst_basetree.tree, width=20)
        svg_string = dg.readwrite.tree.write_svgtree(wrapped_tree)
        outfile.write(base64.b64encode(svg_string))



READ_FUNCTIONS = {
    'codra': dg.read_codra,
    'dis': dg.read_distree,
    'dplp': dg.read_dplp,
    'hilda': dg.read_hilda,
    'hs2015': dg.read_hs2015tree,  # Heilman/Sagae (2015)
    'rs3': dg.read_rs3tree,
    'stagedp': dg.read_stagedp
}

WRITE_FUNCTIONS = {
    'dis': dg.write_dis,
    'rs3': dg.write_rs3,
    'rstlatex': dg.write_rstlatex,
    'tree.prettyprint': write_prettyprinted_nltktree,
    'svgtree': write_svgtree,
    'svgtree-base64': write_nltktree_svg_base64
}


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
                       "Used file keys: {}. Used form fields: {}").format(request.files.keys(), request.form.keys()))
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
                error_msg = u"{0} can't handle input file '{1}'. Got: {2}".format(
                    read_function, input_file.filename, err)
                res = jsonify(error=error_msg, traceback=traceback.format_exc())
                return cors_response(res, 500)

        with tempfile.NamedTemporaryFile() as temp_outputfile:
            if output_format not in WRITE_FUNCTIONS:
                res = jsonify(error="Unknown output format: {}".format(output_format))
                return cors_response(res, 400)

            write_function = WRITE_FUNCTIONS[output_format]

            try:
                write_function(tree, output_file=temp_outputfile.name)
            except Exception as err:
                error_msg = (u"{writer} can't convert ParentedTree to {output_format}. "
                            "Input file '{input_file}'. Got: {error}").format(
                    writer=write_function, output_format=output_format,
                    input_file=input_file.filename, error=err)
                res = jsonify(error=error_msg, traceback=traceback.format_exc())
                return cors_response(res, 500)

            output_filename = "{0}.{1}".format(input_basename, output_format)
            res = send_file(temp_outputfile.name, as_attachment=True,
                            attachment_filename=output_filename)
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


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
