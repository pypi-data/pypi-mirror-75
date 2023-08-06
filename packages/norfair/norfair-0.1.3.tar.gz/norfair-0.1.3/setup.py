# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['norfair']

package_data = \
{'': ['*']}

install_requires = \
['filterpy>=1.4.5,<2.0.0', 'opencv-python>=4.2.0,<5.0.0', 'rich>=5.0.0,<6.0.0']

setup_kwargs = {
    'name': 'norfair',
    'version': '0.1.3',
    'description': 'Simple object tracker',
    'long_description': '# Norfair\n',
    'author': 'joaqo',
    'author_email': 'joaquin.alori@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tryolabs/norfair',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
