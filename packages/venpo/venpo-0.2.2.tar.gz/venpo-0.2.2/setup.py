# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['venpo']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'lxml>=4.5.2,<5.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['venpo = venpo.cli:cli']}

setup_kwargs = {
    'name': 'venpo',
    'version': '0.2.2',
    'description': 'Extract Venmo transactions from a profile with one command',
    'long_description': "# venpo\n\nExtract Venmo transactions from a profile with one command\n\n## Demo\n\nMake demo here\n\n## About\n\nA simple command line tool to extract public Venmo transactions from a specified user profile.\n\nvenpo will access a Venmo user's profile page, extract the transactions, and save to a JSON file.\n\n## Use Cases\n\n1. Save a history of your own or a friend's Venmo transactions\n2. Transaction monitoring for OSINT (open source intelligence) purposes\n3. Collecting data to train your own ML model\n\n\n## Installation\n\n```shell script\n$ pip install venpo --upgrade\n```\n\n## Usage\n\n```shell script\n$ venpo $username\n```",
    'author': 'Marc Ford',
    'author_email': 'mrfxyz567@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mfdeux/venpo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
