# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cotoba_cli', 'cotoba_cli.controller']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.20,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'python-jose>=3.1.0,<4.0.0',
 'pytz>=2020.1,<2021.0',
 'requests>=2.24.0,<3.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['cotoba = cotoba_cli.cli:main']}

setup_kwargs = {
    'name': 'cotoba-cli',
    'version': '1.3.0b1',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
