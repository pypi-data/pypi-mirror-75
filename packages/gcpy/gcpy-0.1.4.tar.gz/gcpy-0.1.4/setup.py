# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcpy',
 'gcpy.firestore',
 'gcpy.functions',
 'gcpy.generators',
 'gcpy.queues',
 'gcpy.tests',
 'gcpy.utils']

package_data = \
{'': ['*']}

install_requires = \
['google.api_core>=1.21.0,<2.0.0', 'google.cloud>=0.34.0,<0.35.0']

setup_kwargs = {
    'name': 'gcpy',
    'version': '0.1.4',
    'description': 'Google Cloud Platform (GCP) Python helpers for functions, queues, collections and more',
    'long_description': None,
    'author': 'Maxim Bazarov',
    'author_email': 'bazaroffma@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
