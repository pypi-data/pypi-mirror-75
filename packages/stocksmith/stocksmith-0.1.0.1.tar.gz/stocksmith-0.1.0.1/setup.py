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
    'version': '0.1.0.1',
    'description': 'Automated tools for stock analysis.',
    'long_description': None,
    'author': 'Saakshaat',
    'author_email': 'saakshaat2001@gmail.com',
    'maintainer': 'Saakshaat',
    'maintainer_email': 'saakshaat2001@gmail.com',
    'url': 'https://github.com/stocksmith/stocksmith/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
