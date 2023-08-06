# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluepdot']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=7.0.0,<8.0.0']

setup_kwargs = {
    'name': 'fluepdot',
    'version': '0.1.1',
    'description': 'A wrapper for the Fluepdot HTTP API',
    'long_description': None,
    'author': 'Carl Gödecken',
    'author_email': 'm@mastercarl.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
