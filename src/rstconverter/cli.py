import argparse
import logging
import sys

from .app import READ_FUNCTIONS, WRITE_FUNCTIONS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='file to be converted')
    parser.add_argument('input_format', help='format of the input file')
    parser.add_argument('output_format', help='format of the output file')
    
    parser.add_argument('output_file', nargs='?', default=sys.stdout)
    
    args = parser.parse_args(sys.argv[1:])

    read_function = READ_FUNCTIONS[args.input_format]

    try:
        tree = read_function(args.input_file)
    except Exception as ex:
        logging.exception("Can't handle input file {}".format(args.input_file))
        sys.exit(1)
    
    write_function = WRITE_FUNCTIONS[args.output_format]
    
    try:
        write_function(tree, output_file=args.output_file)
    except Exception as ex:
        logging.exception("Can't convert input file {} to {}".format(
            args.input_file, args.output_format))


if __name__ == '__main__':
    main()
