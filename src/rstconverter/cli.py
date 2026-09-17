import argparse
import logging
import sys

from .app import READ_FUNCTIONS, WRITE_FUNCTIONS


class FormatParser(argparse.ArgumentParser):
    """An ArgumentParser that reports the supported RST formats on error."""

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, "{prog}: error: {message}\n{formats}\n".format(
            prog=self.prog, message=message, formats=self.format_list()))

    @staticmethod
    def format_list():
        return ("Available input formats: {inputs}\n"
                "Available output formats: {outputs}").format(
                    inputs=', '.join(sorted(READ_FUNCTIONS)),
                    outputs=', '.join(sorted(WRITE_FUNCTIONS)))


def main():
    parser = FormatParser()
    parser.add_argument('input_file', help='file to be converted')
    parser.add_argument('input_format', choices=sorted(READ_FUNCTIONS),
                        help='format of the input file')
    parser.add_argument('output_format', choices=sorted(WRITE_FUNCTIONS),
                        help='format of the output file')
    
    parser.add_argument('output_file', nargs='?', default=None)
    
    args = parser.parse_args(sys.argv[1:])

    read_function = READ_FUNCTIONS[args.input_format]

    try:
        tree = read_function(args.input_file)
    except Exception as ex:
        logging.exception("Can't handle input file {}".format(args.input_file))
        sys.exit(1)

    write_function = WRITE_FUNCTIONS[args.output_format]
    
    output_file = args.output_file if args.output_file is not None else sys.stdout

    try:
        write_function(tree, output_file=output_file)
    except Exception as ex:
        logging.exception("Can't convert input file {} to {}".format(
            args.input_file, args.output_format))


if __name__ == '__main__':
    main()
