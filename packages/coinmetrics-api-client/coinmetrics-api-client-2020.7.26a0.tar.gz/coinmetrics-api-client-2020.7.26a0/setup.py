# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coinmetrics']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['realpython = reader.__main__:main']}

setup_kwargs = {
    'name': 'coinmetrics-api-client',
    'version': '2020.7.26a0',
    'description': 'Python client for Coin Metrics API v4.',
    'long_description': '# Coin Metrics Python API v4 client library\n\nThis is an official Python API client for Coin Metrics API v4.\n',
    'author': 'Coin Metrics',
    'author_email': 'info@coinmetrics.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coinmetrics-io/api-client-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
