# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['queueless']

package_data = \
{'': ['*']}

install_requires = \
['dill', 'psycopg2>=2.8.5,<3.0.0', 'sqlalchemy']

setup_kwargs = {
    'name': 'queueless',
    'version': '0.1.0',
    'description': 'Database-based task management for python',
    'long_description': None,
    'author': 'Exhor',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
