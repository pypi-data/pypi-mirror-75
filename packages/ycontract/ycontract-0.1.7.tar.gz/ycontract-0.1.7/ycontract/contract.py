#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
from dataclasses import dataclass
from inspect import getfile, signature


@dataclass
class ContractState:
    is_enable: bool = True

    def disable(self) -> None:
        self.is_enable = False


SYS_STATE = ContractState()


def disable_contract(state=SYS_STATE) -> None:
    state.disable()


class ContractException(Exception):
    ...


def _new_contract_exception(cond_f, tag, *args, **kw):
    tag_msg = f"tag={tag}\n" if tag else ""
    f_expr = _get_func_expr(cond_f)
    return ContractException(f"Contract Error:\n{f_expr}\n    {tag_msg}args={args},\n    kw={kw}")


def _get_func_expr(f) -> str:
    if '<lambda>' in str(f):
        filename = getfile(f)
        lineno = f.__code__.co_firstlineno
        return f"{filename}:{lineno}"
    else:
        return f.__name__


def prev_contract(cond, tag=None, sys_state=SYS_STATE):

    def _prev_contract(f):

        @functools.wraps(f)
        def wrapped(*args, **kw):
            if sys_state.is_enable:
                f_sig = signature(f)
                binded = f_sig.bind(*args, **kw)
                binded.apply_defaults()
                args, kw = binded.args, binded.kwargs
                if callable(cond):
                    try:
                        if not cond(*args, **kw):
                            raise _new_contract_exception(cond, tag, *args, **kw)
                    except TypeError:
                        f_varnames = list(f_sig.parameters)
                        cond_sig = signature(cond)
                        cond_varnames = list(cond_sig.parameters)
                        varname_indexes = {v: f_varnames.index(v) for v in cond_varnames}

                        def get_arg(v):
                            if varname_indexes[v] < len(args):
                                return args[varname_indexes[v]]
                            elif v in kw:
                                return kw[v]
                            else:
                                return f_sig.parameters[v].default

                        var_args = {v: get_arg(v) for v in cond_sig.parameters.keys()}
                        if not cond(**var_args):
                            raise _new_contract_exception(cond, tag, *args, **kw)
                else:
                    sig = signature(f)
                    binded = sig.bind(*args, **kw)
                    binded.apply_defaults()
                    keys_ = list(binded.arguments.keys())
                    values = list(binded.arguments.values())
                    for varinfo, cond_f in cond.items():
                        if isinstance(varinfo, str):
                            ind = keys_.index(varinfo)
                            if not cond_f(values[ind]):
                                raise _new_contract_exception(cond_f, tag, values[ind])
                        else:
                            inds = []
                            for varname in varinfo:
                                inds.append(keys_.index(varname))
                            cond_arguments = [values[ind] for ind in inds]
                            if not cond_f(*cond_arguments):
                                raise _new_contract_exception(cond_f, tag, *cond_arguments)
            return f(*args, **kw)

        return wrapped

    return _prev_contract


def ret_contract(cond_f, tag=None, sys_state=SYS_STATE):

    def _ret_contract(f):

        @functools.wraps(f)
        def wrapped(*args, **kw):
            result = f(*args, **kw)
            if sys_state.is_enable:
                if not cond_f(result):
                    raise _new_contract_exception(cond_f, tag, result)
            return result

        return wrapped

    return _ret_contract
