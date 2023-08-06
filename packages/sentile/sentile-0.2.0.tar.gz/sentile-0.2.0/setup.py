# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentile', 'sentile.s2', 'sentile.scripts']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['sentile = sentile.scripts.__main__:main']}

setup_kwargs = {
    'name': 'sentile',
    'version': '0.2.0',
    'description': 'Sentinel tile utilities',
    'long_description': None,
    'author': 'Robofarm',
    'author_email': 'hello@robofarm.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
