# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stocksmith']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'stocksmith',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Saakshaat',
    'author_email': 'saakshaat2001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
