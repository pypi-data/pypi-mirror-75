ycontract
================================================================================

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

And if you want to be disable,

``` python
ycontract.SYS_STATE.disable()
```

LICENSES
--------------------------------------------------------------------------------

[Apache 2.0](https://gitlab.com/yassu/ycontract.py/-/blob/master/LICENSE)
