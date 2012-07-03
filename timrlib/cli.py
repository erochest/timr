
"""\
This contains the CLI interface functions.

It handles parsing command-line arguments into an object with the options and
then forwarding everything over to the backend.
"""


__all__ = [
        'main',
        ]


import argparse
from contextlib import nested
import csv
import sys

from timrlib import analysis, http


def validate_args(ap, args):
    """This checks the options objects and raises errors. """


def add_fetch_args(subparser):
    """This adds CLI arguments for the `fetch` command. """
    fetch = subparser.add_parser(
            'fetch',
            help='Download a URL and store the timings.',
            )
    fetch.add_argument(
            '-u', '--url',
            dest='url',
            required=True,
            help='The URL to test.',
            )
    fetch.add_argument(
            '-m', '--message',
            dest='message',
            help='A message for this run.',
            )
    fetch.add_argument(
            '-S', '--no-sha',
            action='store_const',
            dest='use_sha',
            default=True,
            const=False,
            help="Don't use SHA hashing to test the request response.",
            )
    fetch.add_argument(
            '-n', '--times',
            dest='n',
            type=int,
            default=4,
            help='The number of times to download the request. Default is 4.',
            )
    fetch.add_argument(
            '-o', '--output',
            dest='output',
            default='-',
            help='The file to output to. Default is STDOUT.',
            )
    fetch.set_defaults(action='fetch')
    return fetch


def add_report_args(subparser):
    """This adds CLI arguments for the `report` command. """
    report = subparser.add_parser(
            'report',
            help='Print a summary report of a set of timings.',
            )
    report.add_argument(
            '-i', '--input',
            dest='input',
            default='-',
            help='The file containing timings. Default is STDIN.',
            )
    report.add_argument(
            '-o', '--output',
            dest='output',
            default='-',
            help='The file to output to. Default is STDOUT.',
            )
    report.set_defaults(action='report')
    return report


def parse_args(argv):
    """Parse a list of command-line arguments into an object. """
    ap = argparse.ArgumentParser(
            description='Time HTTP requests and analyse the results.',
            fromfile_prefix_chars='@',
            )
    subs = ap.add_subparsers()

    add_fetch_args(subs)
    add_report_args(subs)

    args = ap.parse_args()
    validate_args(ap, args)

    return args


def main(argv=None):
    """The main entry point for the timr script."""
    argv = argv if argv is not None else sys.argv[1:]
    args = parse_args(argv)

    if args.action == 'fetch':
        output = sys.stdout if args.output == '-' else open(args.output, 'ab')
        with output:
            writer = csv.writer(output)
            writer.writerows(http.do_fetch(args))

    elif args.action == 'report':
        inp = sys.stdin if args.input == '-' else open(args.input, 'rb')
        output = sys.stdout if args.output == '-' else open(args.output, 'ab')
        with nested(inp, output):
            reader = csv.reader(inp)
            writer = csv.writer(output)
            writer.writerows(analysis.do_report(http.read_timings(reader)))
