# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openevsewifi']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.10,<2.0.0',
 'pytest-cov>=2.8.1,<3.0.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'openevsewifi',
    'version': '1.1.0',
    'description': 'A python library for communicating with the ESP8266-based wifi module from OpenEVSE',
    'long_description': "# python-openevse-wifi\nA python library for communicating with the ESP8266- and ESP32-based wifi module from OpenEVSE.\nThis library uses RAPI commands over http to query the OpenEVSE charger.\n\nCurrently only supports read-only functionality.\n\n## Installation\nThe easiest way of installing the latest stable version is with pip:\n```\npip install openevsewifi\n```\nThis project uses poetry for dependency management and package publishing.  To install from source using poetry:\n```\npoetry install\n```\nIf you're not planning on doing any development on python-openevse-wifi itself, and you don't want to install poetry, \nyou can also use pip as of version 10.0.  From the root of this repo, run:\n```\npip install .\n```\n\n## Development\nTo set up a development environment, first install Poetry according to the \n[directions](https://python-poetry.org/docs/).\nThen install the dependencies for this project:\n```\npoetry install\n```\nBefore opening a pull request, make sure all tests pass by running `pytest`.\n",
    'author': 'Michelle Avery',
    'author_email': 'dev@miniconfig.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/miniconfig/python-openevse-wifi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
