ycontract
================================================================================

[![PyPI](https://img.shields.io/pypi/v/ycontract)](https://pypi.org/project/exclock/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ycontract)](https://pypi.org/project/exclock/)
[![pipeline status](https://gitlab.com/yassu/ycontract.py/badges/master/pipeline.svg)](https://gitlab.com/yassu/ycontract.py/-/commits/master)
[![coverage report](https://gitlab.com/yassu/ycontract.py/badges/master/coverage.svg)](https://gitlab.com/yassu/ycontract.py/-/commits/master)
[![PyPI - License](https://img.shields.io/pypi/l/ycontract)](https://gitlab.com/yassu/exclock/-/raw/master/LICENSE)


Python library for contracts testing.

This library provides functions for checking argument(`in_contract`) and return value(`out_contract`) of a function.

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
from ycontract import in_contract, out_contract

@in_contract(lambda a, b: a * b > 0)
def add(a, b, c):
    return a + b


@out_contract(lambda res: res > 0)
def sub(a, b):
    return a - b
```

And more complex example for in_contract is

``` python
@in_contract(
    lambda a0: a0 > 0,
    lambda a1, b: a1 > 0 and b > 0,
    {"a2": lambda x: x > 0},
    {("a3",): lambda x: x > 0},
    {("a4", "a5"): lambda x, y: x > 0 and y > 0},
    b=lambda x: x > 0,
)
def add_for_complex(a0, a1, a2, a3, a4, a5, b=1):
    return a0 + a1 + a2 + a3 + a4 + a5 + b
```

Furthermore if you want to be disable, call

``` python
ycontract.disable_contract()
```

LICENSES
--------------------------------------------------------------------------------

[Apache 2.0](https://gitlab.com/yassu/ycontract.py/-/blob/master/LICENSE)
