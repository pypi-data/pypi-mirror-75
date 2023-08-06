# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iprovide']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'iprovide',
    'version': '0.1.1',
    'description': 'Provides a simple but effective  interface definition library.',
    'long_description': None,
    'author': 'David James McCorrie',
    'author_email': 'djmccorrie@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
