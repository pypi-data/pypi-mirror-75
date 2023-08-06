# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acetolang']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['aceto = acetolang:cli']}

setup_kwargs = {
    'name': 'acetolang',
    'version': '1.9.3',
    'description': 'A programming language on a Hilbert curve',
    'long_description': None,
    'author': 'L3viathan',
    'author_email': 'git@l3vi.de',
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
