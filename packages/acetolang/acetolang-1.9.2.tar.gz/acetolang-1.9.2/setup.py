# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acetolang']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0']

entry_points = \
{'console_scripts': ['aceto = acetolang']}

setup_kwargs = {
    'name': 'acetolang',
    'version': '1.9.2',
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
