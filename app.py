import tempfile

from flask import Flask, request
from flask_restplus import Resource, Api

import discoursegraphs as dg

app = Flask(__name__)  # create a Flask app
api = Api(app)  # create a Flask-RESTPlus API


@api.route('/input-formats')
class InputFormats(Resource):
    def get(self):
        # Note: we can't use 'urml' as an input format, because it is
        # based on graphs, while all other formats use trees.
        return sorted(['codra', 'dis', 'dplp', 'hilda', 'rs3'])


@api.route('/output-formats')
class OutputFormats(Resource):
    def get(self):
        return sorted(['dis', 'rs3'])


@api.route('/convert/<string:input_format>/<string:output_format>')
class FormatConverter(Resource):
    """
    curl -XPOST "http://localhost:5000/convert/rs3/dis" -F input_file=@source.rs3
    """
    read_functions = {
        'codra': dg.read_codra,
        'dis': dg.read_distree,
        'dplp': dg.read_dplp,
        'hilda': dg.read_hilda,
        'rs3': dg.read_rs3tree
    }
    
    write_functions = {
        'dis': dg.write_dis,
        'rs3': dg.write_rs3
    }
    
    def post(self, input_format, output_format):
        import pudb; pudb.set_trace()
        input_file = request.files['input_file'] # type: FileStorage
        
        # TODO: is there are spooled named temporary file?
        with tempfile.NamedTemporaryFile() as temp_inputfile:
            temp_inputfile.write(input_file.read())
            
            read_function = self.read_functions[input_format]
            tree = read_function(temp_inputfile.name)
        
        with tempfile.NamedTemporaryFile() as temp_outputfile:
            write_function = self.write_functions[output_format]
            write_function(tree, output_file=temp_outputfile.name)


if __name__ == '__main__':
    app.run(debug=True)
