# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atek_main']

package_data = \
{'': ['*']}

install_requires = \
['cytoolz>=0.10.1,<0.11.0',
 'mysql-connector-python>=8.0.21,<9.0.0',
 'pandas>=1.0.5,<2.0.0',
 'pymysql>=0.10.0,<0.11.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'sshtunnel>=0.1.5,<0.2.0',
 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'atek-main',
    'version': '0.1.5',
    'description': 'Core tools for ATEK',
    'long_description': None,
    'author': 'JediHero',
    'author_email': 'hansen.rusty@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
