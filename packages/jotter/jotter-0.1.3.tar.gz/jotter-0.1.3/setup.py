# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jotter']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'gitpython>=3.1.7,<4.0.0',
 'marshmallow>=3.7.1,<4.0.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['jotter = jotter.cli:jotter']}

setup_kwargs = {
    'name': 'jotter',
    'version': '0.1.3',
    'description': 'Note taking and syncing utility.',
    'long_description': None,
    'author': 'Figglewatts',
    'author_email': 'figglewatts@hotmail.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
