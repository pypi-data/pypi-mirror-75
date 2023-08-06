# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ycontract']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ycontract',
    'version': '0.1.1',
    'description': 'Python library for contracts testing',
    'long_description': 'ycontract\n================================================================================\n',
    'author': 'yassu',
    'author_email': 'yasu0320.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/yassu/ycontract.py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
