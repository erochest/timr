
"""\
This handles downloading resources.
"""


__all__ = [
        'FetchInfo',
        'do_fetch',
        'read_timings',
        ]


from collections import namedtuple
from datetime import datetime
import hashlib
import itertools
import time
import uuid

import requests


FetchInfo = namedtuple(
        'FetchInfo',
        'time, session_id, message, sha, size, elapsed',
        )


def time_call(f, *args, **kwargs):
    """\
    This times a function call and returns the elapsed time and the result.
    """
    start = time.time()
    result = f(*args, **kwargs)
    end = time.time()
    return (end - start, result)


def sha_result(result):
    """This takes the output of time_call and SHA's the result."""
    sha1 = hashlib.sha1()
    sha1.update(result.text.encode('utf8'))
    return sha1.hexdigest()


def sha_skip(_):
    """This skips generating the SHA. """
    return None


def do_fetch(opts):
    """This takes options and downloads the URL N times. """
    session_id = uuid.uuid1()
    now = datetime.now()

    url_seq = itertools.repeat(opts.url, opts.n)
    sha_fn = sha_result if opts.use_sha else sha_skip

    def process(url, now=now, sid=session_id, msg=opts.message):
        (elapsed, result) = time_call(requests.get, url)
        sha = sha_fn(result)
        return FetchInfo(now, sid, msg, sha, len(result.text), elapsed)

    return [process(url) for url in url_seq]


def read_timings(seq):
    """Converst an iter of strings to FetchInfos. """
    for item in seq:
        fi = FetchInfo._make(item)
        yield fi._replace(
                time=datetime.strptime(fi.time, '%Y-%m-%d %H:%M:%S.%f'),
                size=int(fi.size),
                elapsed=float(fi.elapsed),
                )
