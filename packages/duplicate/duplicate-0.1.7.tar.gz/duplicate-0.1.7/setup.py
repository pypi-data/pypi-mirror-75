# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['duplicate']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['duplicate = duplicate.main:cli']}

setup_kwargs = {
    'name': 'duplicate',
    'version': '0.1.7',
    'description': '',
    'long_description': None,
    'author': 'chenn',
    'author_email': 'chenn@gisuni.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
