""" """
from __future__ import unicode_literals, division, print_function, absolute_import
import argparse
import sys

from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData

from sqlacodegen.codegen import CodeGenerator
import sqlacodegen


def main():
    parser = argparse.ArgumentParser(description='Generates SQLAlchemy model code from an existing database.')
    parser.add_argument('url', nargs='?', help='SQLAlchemy url to the database')
    parser.add_argument('--version', action='store_true', help="print the version number and exit")
    parser.add_argument('--schema', help='load tables from an alternate schema')
    parser.add_argument('--tables', help='tables to process (comma-separated, default: all)')
    parser.add_argument('--noviews', action='store_true', help="ignore views")
    parser.add_argument('--noindexes', action='store_true', help='ignore indexes')
    parser.add_argument('--noconstraints', action='store_true', help='ignore constraints')
    parser.add_argument('--nojoined', action='store_true', help="don't autodetect joined table inheritance")
    parser.add_argument('--noinflect', action='store_true', help="don't try to convert tables names to singular form")
    parser.add_argument('--nobackrefs', action='store_true', help="don't include backrefs")
    parser.add_argument('--flask', action='store_true', help="use Flask-SQLAlchemy columns")
    parser.add_argument('--ignorefk', action='store_true', help="Don't check fk constraints on specified columns (comma-separated)")
    parser.add_argument('--dogpile', action='store_true', help="Use dogpile caching. Depends on --flask.")
    parser.add_argument('--outfile', type=argparse.FileType('w'), default=sys.stdout,
                        help='file to write output to (default: stdout)')
    args = parser.parse_args()

    if args.version:
        print(sqlacodegen.version)
        return
    if not args.url:
        print('You must supply a url\n', file=sys.stderr)
        parser.print_help()
        return
    if args.dogpile and not args.flask:
        print('You must use --flask in order to use dogpile option\n', file=sys.stderr)
        parser.print_help()
        return

    engine = create_engine(args.url)
    metadata = MetaData(engine)
    tables = args.tables.split(',') if args.tables else None
    fkcols = args.ignorefk.split(',') if args.ignorefk else None
    metadata.reflect(engine, args.schema, not args.noviews, tables)
    generator = CodeGenerator(metadata, args.noindexes, args.noconstraints,
                              args.nojoined, args.noinflect, args.nobackrefs,
                              args.flask, args.dogpile, fkcols)
    generator.render(args.outfile)
