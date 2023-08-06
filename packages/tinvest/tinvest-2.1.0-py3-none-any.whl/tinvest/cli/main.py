import argparse

from .. import __api_version__, __version__
from ..cli import issues


def run():
    argparser = argparse.ArgumentParser(
        'tinvest', description=f'tinvest {__version__} invest-openapi {__api_version__}'
    )
    argparser.add_argument('command', help='The command to execute')
    argparser.add_argument('arg', nargs='*', help='The arguments of the command')
    args = argparser.parse_args()

    if args.command == 'issues':
        if args.arg == ['openapi']:
            issues.create(issues.Repositories.INVEST_OPENAPI)
        elif not args.arg:
            issues.create()
