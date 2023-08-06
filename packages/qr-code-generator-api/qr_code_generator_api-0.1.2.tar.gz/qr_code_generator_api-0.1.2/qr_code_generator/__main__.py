#!/usr/bin/env python3
from qr_code_generator.wrapper import QrGenerator
import argparse


def main():
    """Main entry function, parses arguments, creates an instance of the wrapper and requests QR codes."""
    parser = create_parser()
    args = parser.parse_args()

    # When an API token is explicitly specified, set it. Else, initialize without token.
    # Also, set the VERBOSE configuration directly here, so we get all logging.
    if args.token:
        api = QrGenerator(args.token, VERBOSE=args.verbose)
    else:
        api = QrGenerator(None, VERBOSE=args.verbose)

    # If a file has been found to load from, load it to data and config:
    if args.load:
        api.load(args.load)

    # If output filename is specified, set filename in app
    if args.output:
        api.output_filename = args.output

    # If bulk requests are made, we should enumerate them and give them specific names
    if args.bulk:
        if api.output_filename:
            name = api.output_filename
            for i in range(1, args.bulk + 1):
                api.output_filename = f'{name}-{i}'
                api.request()
        else:
            for i in range(1, args.bulk + 1):
                api.request()
    else:
        api.request()


def create_parser():
    """
    Create argument parser for command line interface

    Returns
    -------
    parser : ArgumentParser
        The parser with arguments, that will parse the console command
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help='access token for the API', type=str, metavar='')
    parser.add_argument('-l', '--load', help='relative path to yaml file that contains config / data', type=str,
                        metavar='')
    parser.add_argument('-o', '--output', help='output filename without extension', type=str, metavar='')
    parser.add_argument('-b', '--bulk', help='amount of files to generate', type=int, metavar='')
    parser.add_argument('-v', '--verbose', help='whether or not program logs should show', action='store_true')
    # parser.add_argument('--disable_traceback', help='disable showing of Python traceback', action='store_true')
    # parser.add_argument('-d', '--debug', help='whether or not debug logs should show', action='store_true')
    return parser


if __name__ == "__main__":
    """Main entry point, calls main entry function"""
    main()
