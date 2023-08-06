# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cotoba_cli']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0',
 'click>=7.0,<8.0',
 'python-jose>=3.0,<4.0',
 'pytz>=2019,<2020',
 'requests>=2.21,<3.0',
 'toml>=0,<1']

entry_points = \
{'console_scripts': ['cotoba = cotoba_cli.cli:main']}

setup_kwargs = {
    'name': 'cotoba-cli',
    'version': '1.2.1b1',
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
