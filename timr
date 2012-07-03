#!/usr/bin/env python


import argparse
import csv
import datetime
import hashlib
import sys
import time

import requests


N = 4

SITE = 'http://neatline.dev/'
NL = SITE + 'neatline-exhibits/'
MAIN = NL + 'show/battle-of-chancellorsville'
JSON = NL + 'openlayers/9'

URLS = [
        # MAIN,
        JSON,
        ]


MAIN_SHA = '3fd4259f5a8afd26df5dfe8f217876c8dff755df'
JSON_SHA = 'f31167c15235bdf9a51ad42d342f444a37530f3e'


def time_url(url):
    """Time downloading a URL and digest the content. """
    start = time.time()
    resp = requests.get(url)
    end = time.time()

    sha1 = hashlib.sha1()
    sha1.update(resp.text)

    return (end - start, len(resp.text), sha1.hexdigest())


def parse_args(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--message', type=str, default=None,
                        dest='message',
                        help='A message for the output.')
    parser.add_argument('n', metavar='N', type=int, default=N, nargs='?',
                        help='The number of downloads to time.')
    args = parser.parse_args()
    return args


def process_urls(n, msg, *urls):
    times = xrange(n)
    for url in urls:
        for _ in times:
            now = datetime.datetime.now()
            (elapsed, size, hash) = time_url(url)
            yield (url, now, elapsed, size, hash, msg)


def main(argv=None):
    args = parse_args(argv)

    writer = csv.writer(sys.stdout)
    writer.writerows(process_urls(args.n, args.message, *URLS))


if __name__ == '__main__':
    main()
