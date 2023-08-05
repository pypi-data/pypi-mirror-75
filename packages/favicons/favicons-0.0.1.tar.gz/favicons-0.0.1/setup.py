# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['favicons', 'favicons._types']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1,<8.0', 'pillow>=7.2,<8.0', 'rich>=3.3.2,<4.0.0']

setup_kwargs = {
    'name': 'favicons',
    'version': '0.0.1',
    'description': 'Favicon generator for Python',
    'long_description': None,
    'author': 'checktheroads',
    'author_email': 'matt@allroads.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
