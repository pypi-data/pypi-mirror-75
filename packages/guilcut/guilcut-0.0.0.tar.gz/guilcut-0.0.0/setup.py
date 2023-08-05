# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guilcut']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'guilcut',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'shokoysn',
    'author_email': 'syokoysn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
