#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
  test [--day=<day>] [--hour=<hour>] [--minutes=<minutes>]
  test --version
  test -h | --help

Options:
  -h --help            Show this screen.
  --version            Show version.
  --day=<day>          How many days ago [default: 0].
  --hour=<hour>        How many hours ago [default: 0].
  --minutes=<minutes>  How many minutes ago [default: 0].

"""
import sys
from docopt import docopt
from schema import Schema, SchemaError, And, Or, Use

# schemaで値の型チェック
def validate_args(args):
    schema = Schema({
        '--day': Or(None, And(Use(int), lambda n: 0 <= n), error="-n should be positive integer"),
        '--hour': Or(None, And(Use(int), lambda n: 0 <= n), error="-n should be positive integer"),
        '--minutes': Or(None, And(Use(int), lambda n: 0 <= n), error="-n should be positive integer"),
        '--help': bool,
        '--version': bool
    })

    return schema.validate(args)


# docoptでusage設定
def usage():
    args = docopt(__doc__, version="0.0.1")

    try:
        return validate_args(args)
    except SchemaError as error:
        print(error)
        sys.exit(1)


usage()
