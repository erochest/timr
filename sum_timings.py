#!/usr/bin/env python

import csv
import itertools
import math
import operator
import sys

import clint


HEADER = (
        'message',
        'min',
        'max',
        'mean',
        's'
        )

get_elapsed = operator.itemgetter(2)
get_msg = operator.itemgetter(5)


def proc_file(filename):
    with open(filename, 'rb') as fin:
        reader = csv.reader(fin)
        for (msg, group) in itertools.groupby(reader, get_msg):
            elapsed = [float(get_elapsed(obs)) for obs in group]
            n = float(len(elapsed))
            mean = sum(elapsed) / n
            stddev = math.sqrt(
                    (1 / (n - 1)) * sum((e - mean) ** 2 for e in elapsed)
                    )
            yield (
                    msg,
                    min(elapsed),
                    max(elapsed),
                    mean,
                    stddev,
                    )


def report(summaries):
    writer = csv.writer(sys.stdout, csv.excel_tab)
    writer.writerow(HEADER)
    writer.writerows(summaries)


def main():
    file_summaries = itertools.imap(proc_file, clint.args.files)
    report(itertools.chain.from_iterable(file_summaries))

if __name__ == '__main__':
    main()
