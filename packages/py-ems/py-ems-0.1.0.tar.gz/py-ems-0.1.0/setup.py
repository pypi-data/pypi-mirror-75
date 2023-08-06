# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyems']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0', 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'py-ems',
    'version': '0.1.0',
    'description': 'High-level python interface to OpenEMS with automatic mesh generation',
    'long_description': None,
    'author': 'Matt Huszagh',
    'author_email': 'huszaghmatt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
