
# `timr`

This is a utility for timing how long it takes to access an HTTP resource and
for generating summary statistics about that.

I was working on a project and needed to optimize how long it took to download
a resource. Of course, optimizing anything is difficult without good numbers.
This script was a way to track the times and generate some semi-useful data
about them.

## Installation

    pip install timr

## Usage

Generally, before you start optimizing your resource, you'll need a baseline:

```bash
timr fetch -u http://mysite-wow.org -m "initial timing" -n10 -otimings.csv
```

You'll run something like this a lot. Let's optimize it by pulling the options
that won't change into a file. We'll call it `fetch.cfg`.

    --url
    http://mysite-wow.org
    --times
    10
    --output
    timings.csv

Now we can refer to that file on the command line using a `@` prefix:

```bash
timr fetch @fetch.cfg -m "initial timing"
```

From this point on, after making a change, re-run this with a different
message:

```bash
timr fetch @fetch.cfg -m "improved caching"
```

When you want to get an idea of how things are going, run the `report` task:

```bash
timr report --input timings.csv --output summary.csv
```

For more information about the fields in these files, see the sections about
those tasks below.

## Tasks

### `fetch`

```bash
$ timr fetch --help

usage: timr fetch [-h] -u URL [-m MESSAGE] [-S] [-n N] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     The URL to test.
  -m MESSAGE, --message MESSAGE
                        A message for this run.
  -S, --no-sha          Don't use SHA hashing to test the request response.
  -n N, --times N       The number of times to download the request. Default
                        is 4.
  -o OUTPUT, --output OUTPUT
                        The file to output to. Default is STDOUT.
```

This downloads the resource in `--url` `--times` times. Optionally, each time
it computes a SHA hash of the result, so you can make sure nothing changes.

The output is CSV and has these fields:

* `time` — A timestamp for the run.
* `session_id` — A globally unique ID for tracking this run.
* `message` — A message describing this run. This is set with the `--message`
  argument.
* `sha` — The SHA hash of the response.
* `size` — The number of characters in the response.
* `elapsed` — The number of seconds the response took.

### `report`

```bash
usage: timr report [-h] [-i INPUT] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        The file containing timings. Default is STDIN.
  -o OUTPUT, --output OUTPUT
                        The file to output to. Default is STDOUT.
```

This takes the output of the `fetch` task and creates some statistics.

The output is CSV and has these fields:

* `session_id` — The globally unique session ID.
* `message` — The message describing the run, set when running `fetch`.
* `min` — The minimum elapsed time for the run.
* `max` — The maximum elapsed time for the run.
* `mean` — The mean elapsed time for the run.
* `s` — The estimated sample standard deviation from the mean for the run.

## TODOs

* Add the option to run `fetch` in parallel.

## Issues

Please leave them on the [issue tracker](https://github.com/erochest/timr).

