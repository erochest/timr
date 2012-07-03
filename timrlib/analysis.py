
"""\
This takes the output of the timings and generates some summary data.

"""


from collections import namedtuple
import itertools
import math
import operator


SummaryData = namedtuple(
        'SummaryData',
        'session_id, message, min, max, mean, s',
        )


get_session_id = operator.attrgetter('session_id')


def do_report(input):
    """This takes a sequence of FetchInfo and generates SummaryDatas."""
    for (session_id, group) in itertools.groupby(input, get_session_id):
        group = list(group)
        elapsed = [finfo.elapsed for finfo in group]
        n = float(len(elapsed))
        mean = sum(elapsed) / n
        s = math.sqrt(
                (1 / (n - 1)) * sum((e - mean) ** 2 for e in elapsed)
                )
        yield SummaryData(
                session_id,
                group[0].message,
                min(elapsed),
                max(elapsed),
                mean,
                s
                )
