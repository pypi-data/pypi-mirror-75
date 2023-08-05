# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cad_tickers', 'cad_tickers.exchanges']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'coverage>=5.2,<6.0',
 'lxml>=4.5.2,<5.0.0',
 'pandas>=1.0.5,<2.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'cad-tickers',
    'version': '0.1.3',
    'description': 'Various Stock Utilties Created by me',
    'long_description': "## Cad Tickers\n\nSet of utilities modules designed to scrap data from the web.\n\nWill write more documentation later, for now refer to test cases.\n\n\nFor the tsx searching, it was kinda tedious to test each of the possible values, as a result, only `exchanges` and `marketcap` values are validated.\n\nGiven the new redesign of the web.tmxmoney site, don't expect the existing api to work\nfor a super long period of time.\n\nSupport will be provided to the best of my ability.\n\n### How to run tests\n\n```\npytest\n```\n\n#### Todo\n\n* add just read the docs\n",
    'author': 'David Li',
    'author_email': 'davidli012345@gmail.com',
    'maintainer': 'David Li',
    'maintainer_email': 'davidli012345@gmail.com',
    'url': 'https://github.com/FriendlyUser/cad_tickers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
