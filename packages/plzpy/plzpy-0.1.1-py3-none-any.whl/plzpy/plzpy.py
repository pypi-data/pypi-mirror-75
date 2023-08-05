#!/usr/bin/env python3

# Copyright © 2020 Andrea Giacobino <no.andrea@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from . import _version
import argparse
import csv
import time
import os
import json
# flask
from flask import Flask, jsonify
from flask_cors import cross_origin
from waitress import serve as _serve


# keys for accessing data

KEY_COUNTERS = "counters"
KEY_DISTRIB = "distributions"


def massage(csvPath: str, jsonPath: str, summary: bool):
    """
    Process the dataset csv input to a json optimized
    for the rest API to serve

    Args:
        csvPath(str): the path of the input csv file
        jsonPath(str): the path of the output json file
        summary(bool): if True only print summary of data processing
    """
    print(f"Input file is ", csvPath)
    # track the execution time
    start = time.time()
    # print file size
    print(f"Input file size (gb) is {float(os.stat(csvPath).st_size) / 1e9:.4f}")
    # read csv file
    cZip, cYear = "PLZ", "STR_DATUM"
    aggregate = {}  # this holds zip[year]=count
    with open(csvPath) as fp:
        x = 0
        for row in csv.DictReader(fp):
            z, y = row[cZip], row[cYear][0:4]
            zd = aggregate.get(z)
            # if there is no zip, add one
            if zd is None:
                aggregate[z] = {y: 1}
                continue
            # otherwise just increment
            c = zd.get(y, 0)
            aggregate[z][y] = c + 1
            # print progress
            x += 1
            if not summary:
                print(f"\rRecord {x}", end="")
    print(f"Processed {x} records")
    print(f"Data read after {time.time() - start}")

    # step 2 prepare json output
    counter, distrib = {}, {}  # final outputs
    for z, ycm in aggregate.items():
        _sum = 0
        ycl = []  # list of year/count
        for y, c in ycm.items():
            _sum += c  # add the count to the sum
            ycl.append({"year": y, "count": c})
        # sort the result
        ycl = sorted(ycl, key=lambda yc: yc["year"])
        # and prepare for output
        counter[z] = {"total": _sum}
        distrib[z] = ycl
    # finally write the output
    with open(jsonPath, "w") as fp:
        json.dump({KEY_COUNTERS: counter, KEY_DISTRIB: distrib}, fp, indent=2)

    print(f"Output size(gb) is {float(os.stat(jsonPath).st_size) / 1e9: .4f}")
    print(f"Output written at {jsonPath}")
    print(f"Completed in {time.time() - start}")


def cmd_massage(args):
    """
    Massage the dataset
    """
    try:
        massage(args.input, args.output, args.summary)
    except Exception as err:
        print(f"Error massaging data: {err}")


def serve(dataFile: str, address: str):
    address, port = address.split(":")
    port = 2007 if port is None else int(port)
    # load the data file
    with open(dataFile) as fp:
        data = json.load(fp)

    app = Flask(__name__, static_url_path='')

    @app.route('/status')
    @cross_origin()
    def status():
        return jsonify({
            "status": "ok",
            "version": _version(),
            "zip_codes": len(data[KEY_COUNTERS])
        })

    @app.route("/zip/buildings")
    @cross_origin()
    def buildings():
        return jsonify(data[KEY_COUNTERS])

    @app.route("/zip/buildings/<code>")
    @cross_origin()
    def buildings_filter(code: str):
        v = data[KEY_COUNTERS].get(code)
        if v is None:
            return jsonify({}), 404
        return jsonify(v)

    @app.route("/zip/buildings/history")
    @cross_origin()
    def history():
        return jsonify(data[KEY_DISTRIB])

    @app.route("/zip/buildings/<code>/history")
    @cross_origin()
    def history_filter(code: str):
        v = data[KEY_DISTRIB].get(code)
        if v is None:
            return jsonify({}), 404
        return jsonify(v)

    _serve(app, host=address, port=port)
    pass


def cmd_serve(args):
    """
    Serve the api
    """
    try:
        serve(args.data, args.listen)
    except Exception as err:
        print(f"Error serving data: {err}")


def cmd_version(args):
    """
    Print the version and exit
    """
    print(f"plzpy v{_version()}")


def main():
    commands = [
        {
            'name': 'massage',
            'help': 'Transform data from ESRI CSV to JSON suitable for serving zip info',
            'target': cmd_massage,
            'opts': [
                {
                    "names": ["-i", "--input"],
                    "help": "The input csv file (default data.csv)",
                    "default": "data.csv"
                },
                {
                    "names": ["-o", "--output"],
                    "help": "The output json file (default data.json)",
                    "default": "data.json"
                },
                {
                    "names": ["-s", "--summary"],
                    "help": "Print only execution summary",
                    "default": False,
                    "action": "store_true",
                },

            ]
        },
        {
            'name': 'serve',
            'help': 'Serve the dataset from a json file',
            'target': cmd_serve,
            'opts': [
                {
                    "names": ["--data"],
                    "help": "the json dataset to serve",
                    "default": "data.json"
                },
                {
                    "names": ["--listen"],
                    "help": "The address to listen to (default 0.0.0.0:2007)",
                    "default": "0.0.0.0:2007"
                }
            ]
        },
        {
            'name': 'version',
            'help': 'Print the version and exit',
            'target': cmd_version,
            'opts': [
            ]
        },

    ]
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = 'command'
    # register all the commands
    for c in commands:
        subparser = subparsers.add_parser(c['name'], help=c['help'])
        subparser.set_defaults(func=c['target'])
        # add the sub arguments
        for sa in c.get('opts', []):
            subparser.add_argument(*sa['names'],
                                   help=sa['help'],
                                   action=sa.get('action'),
                                   default=sa.get('default'))

    # parse the arguments
    args = parser.parse_args()
    # call the function
    args.func(args)


if __name__ == "__main__":
    main()
