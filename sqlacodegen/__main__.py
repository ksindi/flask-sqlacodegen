#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generates SQLAlchemy model code from an existing database.

Prompt parameters:
  url:              SQLAlchemy url to the database
  fetched-value:    use FetchValue for columns with server default
  flask:            use Flask SQLAclhemy for model generation
  ignore-cols:      don't check foreign key constraints on specified columns
  log-level (-l)    logging level (default=INFO)
  noclasses:        don't generate classes, only tables
  noconstraints:    ignore constraints
  noindexes:        ignore indexes
  noinflect:        don't try to convert tables names to singular form
  nojoined:         don't autodetect joined table inheritance
  noviews:          ignore views
  outfile (-o):     file to write output to (default: stdout)
  schema:           load tables from an alternate schema
  table (-t):       tables to process (comma-separated, default: all)
  version (-v):     print the version number and exit

Usage:
  flask-sqlacodegen mysql+mysqldb://uname:passwd@localhost/dbname --flask
"""
from __future__ import unicode_literals, print_function, absolute_import

import logging
import sys
from argparse import RawDescriptionHelpFormatter, ArgumentParser, FileType

import pkg_resources
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData

from sqlacodegen.codegen import CodeGenerator

logger = logging.getLogger(__name__)
LOGFORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'


def create_parser():
    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('url', metavar='DATABASE_URL')
    parser.add_argument('--fetched-value', action='store_true')
    parser.add_argument('--flask', action='store_true')
    parser.add_argument('--ignore-cols', nargs='*')
    parser.add_argument('--log-level', '-l', type=str.upper, default='INFO')
    parser.add_argument('--noviews', action='store_true')
    parser.add_argument('--noindexes', action='store_true')
    parser.add_argument('--noconstraints', action='store_true')
    parser.add_argument('--nojoined', action='store_true')
    parser.add_argument('--noinflect', action='store_true')
    parser.add_argument('--noclasses', action='store_true')
    parser.add_argument('--outfile', '-o', nargs='?', type=FileType('w'),
                        default=sys.stdout)
    parser.add_argument('--schema')
    parser.add_argument('--tables', '-t', nargs='*')
    parser.add_argument('--version', '-v', action='store_true')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    print("Args: ", args)

    numeric_level = getattr(logging, args.log_level, None)
    logging.basicConfig(format=LOGFORMAT)
    logger.setLevel(numeric_level)

    if args.version:
        pkg_name = 'flask-sqlacodegen'
        version = pkg_resources.get_distribution(pkg_name).parsed_version
        logger.info(version.public)
        return

    engine = create_engine(args.url)
    metadata = MetaData(engine)
    metadata.reflect(engine, args.schema, not args.noviews, args.tables)
    generator = CodeGenerator(**vars(args))
    generator.render(args.outfile)
