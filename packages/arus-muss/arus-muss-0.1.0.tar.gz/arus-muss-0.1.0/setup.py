# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arus_muss', 'arus_muss.tests']

package_data = \
{'': ['*'], 'arus_muss': ['models/*']}

install_requires = \
['arus>=1.1.12,<2.0.0']

entry_points = \
{'console_scripts': ['arus-muss = arus_muss.cli:cli']}

setup_kwargs = {
    'name': 'arus-muss',
    'version': '0.1.0',
    'description': 'Package for MUSS activity recognition algorithm (see doi: 10.1249/MSS.0000000000002306 for the description of the algorithm).',
    'long_description': None,
    'author': 'Qu Tang',
    'author_email': 'tang.q@northeastern.edu',
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
