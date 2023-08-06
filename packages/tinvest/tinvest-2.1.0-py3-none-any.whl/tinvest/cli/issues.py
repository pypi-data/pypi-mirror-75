import platform
import urllib.parse
import webbrowser
from enum import Enum

from .. import __api_version__, __version__

GITHUB = 'https://github.com'


class Repositories(str, Enum):
    TINVEST = '/daxartio/tinvest'
    INVEST_OPENAPI = '/TinkoffCreditSystems/invest-openapi'


def create(repo: Repositories = Repositories.TINVEST):
    params = {
        'body': (
            '## Expected Behavior\n\n\n\n'
            '## Actual Behavior\n\n\n\n'
            '## Steps to Reproduce the Problem\n\n'
            '  1. \n'
            '  1. \n'
            '  1. \n\n'
            '## Specifications\n\n'
            f'  - **[tinvest](/daxartio/tinvest/)** {__version__}\n'
            '  - **[invest-openapi](/TinkoffCreditSystems/invest-openapi/)** '
            f'{__api_version__}\n'
            f'  - **platform** {platform.platform()}\n'
        ),
    }

    query = urllib.parse.urlencode(params)
    url = f'{GITHUB}{repo}/issues/new?{query}'

    webbrowser.open(url, new=2)
