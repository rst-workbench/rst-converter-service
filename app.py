import codecs
import tempfile
import traceback
from pathlib2 import Path

from flask import jsonify, Flask, request, send_file
from flask_restplus import Resource, Api
from nltk.treeprettyprinter import TreePrettyPrinter

import discoursegraphs as dg

app = Flask(__name__)  # create a Flask app
api = Api(app)  # create a Flask-RESTPlus API


def write_prettyprinted_nltktree(rst_basetree, output_file):
    with codecs.open(output_file, 'w', 'utf-8') as outfile:
        outfile.write(TreePrettyPrinter(rst_basetree.tree).text())


READ_FUNCTIONS = {
    'codra': dg.read_codra,
    'dis': dg.read_distree,
    'dplp': dg.read_dplp,
    'hilda': dg.read_hilda,
    'hs2015': dg.read_hs2015tree,  # Heilman/Sagae (2015)
    'rs3': dg.read_rs3tree
}

WRITE_FUNCTIONS = {
    'dis': dg.write_dis,
    'rs3': dg.write_rs3,
    'tree': write_prettyprinted_nltktree,
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
    # FIXME: add support for hs2015 format

    def post(self, input_format, output_format):
        """Convert from one RST format to another.

        Usage example:

            curl -XPOST "http://localhost:5000/convert/rs3/dis" -F input_file=@source.rs3
        """
        if 'input_file' not in request.files:
            res = jsonify(
                error=("Please upload a file using the key "
                       "'input_file'. Used file key(s): {}").format(request.files.keys()))
            res.status_code = 500
            return res

        input_file = request.files['input_file']  # type: FileStorage
        input_basename = Path(input_file.filename).stem

        with tempfile.NamedTemporaryFile() as temp_inputfile:
            input_file.save(temp_inputfile.name)

            if input_format not in READ_FUNCTIONS:
                res = jsonify(error="Unknown input format: {}".format(input_format))
                res.status_code = 400
                return res

            read_function = READ_FUNCTIONS[input_format]

            try:
                tree = read_function(temp_inputfile.name)
            except Exception as err:
                error_msg = u"{0} can't handle input file '{1}'. Got: {2}".format(
                    read_function, input_file.filename, err)
                res = jsonify(error=error_msg, traceback=traceback.format_exc())
                res.status_code = 500
                return res

        with tempfile.NamedTemporaryFile() as temp_outputfile:
            if output_format not in WRITE_FUNCTIONS:
                res = jsonify(error="Unknown output format: {}".format(output_format))
                res.status_code = 400
                return res

            write_function = WRITE_FUNCTIONS[output_format]

            try:
                write_function(tree, output_file=temp_outputfile.name)
            except Exception as err:
                error_msg = (u"{writer} can't convert ParentedTree to {output_format}. "
                            "Input file '{input_file}'. Got: {error}").format(
                    writer=write_function, output_format=output_format,
                    input_file=input_file.filename, error=err)
                res = jsonify(error=error_msg, traceback=traceback.format_exc())
                res.status_code = 500
                return res

            output_filename = "{0}.{1}".format(input_basename, output_format)
            res = send_file(temp_outputfile.name, as_attachment=True,
                            attachment_filename=output_filename)
        return res


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
