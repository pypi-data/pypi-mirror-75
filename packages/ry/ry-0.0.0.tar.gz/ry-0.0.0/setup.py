# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ry',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'ryan',
    'author_email': 'ryan?@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
