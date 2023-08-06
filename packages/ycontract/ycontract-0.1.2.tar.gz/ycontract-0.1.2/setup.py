# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ycontract']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ycontract',
    'version': '0.1.2',
    'description': 'Python library for contracts testing',
    'long_description': 'ycontract\n================================================================================\n\nPython library for contracts testing\n\nHow to install\n--------------------------------------------------------------------------------\n\n``` sh\n$ pip install ycontract\n```\n\nExample\n--------------------------------------------------------------------------------\n\nExample files are [here](https://gitlab.com/yassu/ycontract.py/-/blob/master/tests/test_contract.py)(test files)\n\nAnd if you want to be disable,\n\n``` python\nycontract.SYS_STATE.disable()\n```\n\nLICENSES\n--------------------------------------------------------------------------------\n\n[Apache 2.0](https://gitlab.com/yassu/ycontract.py/-/blob/master/LICENSE)\n',
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
