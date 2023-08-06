# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['venpo']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'lxml>=4.5.2,<5.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['venpo = venpo.cli:cli']}

setup_kwargs = {
    'name': 'venpo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Marc Ford',
    'author_email': 'mrfxyz567@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
