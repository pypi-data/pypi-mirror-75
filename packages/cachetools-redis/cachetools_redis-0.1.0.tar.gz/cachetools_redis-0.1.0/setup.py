# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cachetools_redis']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=4.1.1,<5.0.0', 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'cachetools-redis',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Anish Padhi',
    'author_email': 'padhi.anish@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
