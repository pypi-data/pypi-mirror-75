# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['setup_utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'setup-utils',
    'version': '0.2.0',
    'description': 'Python Setup Utilities',
    'long_description': None,
    'author': 'skeptycal',
    'author_email': '26148512+skeptycal@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
