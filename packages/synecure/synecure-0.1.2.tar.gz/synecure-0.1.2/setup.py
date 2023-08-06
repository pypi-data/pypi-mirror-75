# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synecure']

package_data = \
{'': ['*']}

install_requires = \
['coleo>=0.1.5,<0.2.0']

entry_points = \
{'console_scripts': ['bsync = synecure.cli:entry_bsync',
                     'sy = synecure.cli:entry_sy',
                     'sy-config = synecure.cli:entry_sy_config']}

setup_kwargs = {
    'name': 'synecure',
    'version': '0.1.2',
    'description': 'File sync utility',
    'long_description': None,
    'author': 'Olivier Breuleux',
    'author_email': 'breuleux@gmail.com',
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
