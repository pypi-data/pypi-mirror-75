# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ycontract']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ycontract',
    'version': '0.2.1',
    'description': 'Python library for contracts testing',
    'long_description': 'ycontract\n================================================================================\n\n[![PyPI](https://img.shields.io/pypi/v/ycontract)](https://pypi.org/project/exclock/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ycontract)](https://pypi.org/project/exclock/)\n[![pipeline status](https://gitlab.com/yassu/ycontract.py/badges/master/pipeline.svg)](https://gitlab.com/yassu/ycontract.py/-/commits/master)\n[![coverage report](https://gitlab.com/yassu/ycontract.py/badges/master/coverage.svg)](https://gitlab.com/yassu/ycontract.py/-/commits/master)\n[![PyPI - License](https://img.shields.io/pypi/l/ycontract)](https://gitlab.com/yassu/exclock/-/raw/master/LICENSE)\n\n\nPython library for contracts testing.\n\nThis library provides functions for precondition(`in_contract`) and postcondition(`out_contract`).\n\nHow to install\n--------------------------------------------------------------------------------\n\n``` sh\n$ pip install ycontract\n```\n\nExample\n--------------------------------------------------------------------------------\n\nExample files are [here](https://gitlab.com/yassu/ycontract.py/-/blob/master/tests/test_contract.py)(test file)\n\nMain example is\n\n``` python\nfrom ycontract import in_contract, out_contract\n\n@in_contract(lambda a, b: a * b > 0)\ndef add(a, b, c, d=2, e=3):\n    return a + b + c + d + e\n\n\n@out_contract(lambda res: res > 0)\ndef sub(a, b):\n    return a - b\n```\n\nAnd if you want to be disable, call\n\n``` python\nycontract.disable_contract()\n```\n\nLICENSES\n--------------------------------------------------------------------------------\n\n[Apache 2.0](https://gitlab.com/yassu/ycontract.py/-/blob/master/LICENSE)\n',
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
