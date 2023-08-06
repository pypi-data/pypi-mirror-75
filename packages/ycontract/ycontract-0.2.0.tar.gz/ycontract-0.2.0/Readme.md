ycontract
================================================================================

[![PyPI](https://img.shields.io/pypi/v/ycontract)](https://pypi.org/project/exclock/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ycontract)](https://pypi.org/project/exclock/)
[![pipeline status](https://gitlab.com/yassu/ycontract.py/badges/master/pipeline.svg)](https://gitlab.com/yassu/ycontract.py/-/commits/master)
[![coverage report](https://gitlab.com/yassu/ycontract.py/badges/master/coverage.svg)](https://gitlab.com/yassu/ycontract.py/-/commits/master)
[![PyPI - License](https://img.shields.io/pypi/l/ycontract)](https://gitlab.com/yassu/exclock/-/raw/master/LICENSE)


Python library for contracts testing.

This library provides functions for precondition(`prev_contract`) and postcondition(`ret_contract`).

How to install
--------------------------------------------------------------------------------

``` sh
$ pip install ycontract
```

Example
--------------------------------------------------------------------------------

Example files are [here](https://gitlab.com/yassu/ycontract.py/-/blob/master/tests/test_contract.py)(test file)

Main example is

``` python
from ycontract import prev_contract, ret_contract

@prev_contract(lambda a, b: a * b > 0)
def add(a, b, c, d=2, e=3):
    return a + b + c + d + e


@ret_contract(lambda res: res > 0)
def sub(a, b):
    return a - b
```

And if you want to be disable, call

``` python
ycontract.disable_contract()
```

LICENSES
--------------------------------------------------------------------------------

[Apache 2.0](https://gitlab.com/yassu/ycontract.py/-/blob/master/LICENSE)
