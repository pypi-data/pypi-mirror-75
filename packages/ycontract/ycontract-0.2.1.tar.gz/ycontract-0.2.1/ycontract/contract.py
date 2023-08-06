#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
from dataclasses import dataclass
from inspect import getfile, getsource, signature
from typing import Callable, Optional


@dataclass
class ContractState:
    is_enable: bool = True

    def disable(self) -> None:
        self.is_enable = False


SYS_STATE = ContractState()


def disable_contract(state: ContractState = SYS_STATE) -> None:
    state.disable()


class ContractException(Exception):
    ...


def _new_contract_exception(cond_f: Callable[..., bool], tag: Optional[str], *args, **kw):
    tag_msg = f"tag={tag}\n" if tag else ""
    f_expr = _get_func_expr(cond_f)
    return ContractException(f"Contract Error:\n{f_expr}\n    {tag_msg}args={args},\n    kw={kw}")


def _get_func_expr(f: Callable) -> str:
    if '<lambda>' in str(f):
        filename = getfile(f)
        lineno = f.__code__.co_firstlineno
        source = getsource(f)
        return f"{filename}:{lineno}:{source}"
    else:
        lineno = f.__code__.co_firstlineno
        return f"{f.__name__}:{lineno}"


def __in_contract_callable_full_match_case(
        cond_f: Callable[..., bool], f: Callable, tag: Optional[str], sys_state: ContractState,
        *args, **kw):
    return cond_f(*args, **kw)


def __in_contract_callable_partial_match_case(
        cond_f: Callable[..., bool], f: Callable, tag: Optional[str], sys_state: ContractState,
        *args, **kw):
    f_sig = signature(f)
    f_varnames = list(f_sig.parameters)
    cond_sig = signature(cond_f)
    cond_varnames = list(cond_sig.parameters)
    varname_indexes = {v: f_varnames.index(v) for v in cond_varnames}

    def get_arg(v: str):
        if varname_indexes[v] < len(args):
            return args[varname_indexes[v]]
        elif v in kw:
            return kw[v]
        else:
            return f_sig.parameters[v].default

    var_args = {v: get_arg(v) for v in cond_sig.parameters.keys()}

    return cond_f(**var_args)


def __in_contract_callable_one(
        cond_f: Callable[..., bool], f: Callable, tag: Optional[str], sys_state: ContractState,
        *args, **kw):
    try:
        return __in_contract_callable_full_match_case(cond_f, f, tag, sys_state, *args, **kw)
    except TypeError:
        return __in_contract_callable_partial_match_case(cond_f, f, tag, sys_state, *args, **kw)


def __in_contract_dict_match_varname_case(
        varname: str, cond_f: Callable[..., bool], f: Callable, tag: Optional[str],
        sys_state: ContractState, *args, **kw):
    sig = signature(f)
    binded = sig.bind(*args, **kw)
    binded.apply_defaults()
    keys_ = list(binded.arguments.keys())
    values = list(binded.arguments.values())
    ind = keys_.index(varname)
    is_ok = cond_f(values[ind])
    if is_ok:
        return True
    else:
        return values[ind]


def _get_contract_extion_from_dict(
        cond_f: Callable[..., bool], f: Callable, varinfo, tag: Optional[str],
        sys_state: ContractState, *args, **kw) -> Optional[ContractException]:
    if isinstance(varinfo, str):
        res = __in_contract_dict_match_varname_case(
            varinfo, cond_f, f, tag, sys_state, *args, **kw)
        if res is not True:
            return _new_contract_exception(cond_f, tag, res)
    else:
        f_sig = signature(f)
        binded = f_sig.bind(*args, **kw)
        binded.apply_defaults()
        args, kw = binded.args, binded.kwargs
        keys_ = list(binded.arguments.keys())
        values = list(binded.arguments.values())
        inds = []
        for varname in varinfo:
            inds.append(keys_.index(varname))
        cond_arguments = [values[ind] for ind in inds]
        if not cond_f(*cond_arguments):
            return _new_contract_exception(cond_f, tag, *cond_arguments)

    return None


def in_contract(
        *conds, tag: Optional[str] = None, sys_state: ContractState = SYS_STATE, **cond_opts):

    def _in_contract(f: Callable):

        @functools.wraps(f)
        def wrapped(*args, **kw):
            if sys_state.is_enable:

                for cond in conds:
                    if callable(cond):
                        if not __in_contract_callable_one(cond, f, tag, sys_state, *args, **kw):
                            raise _new_contract_exception(cond, tag, *args, **kw)
                    else:
                        for varinfo, cond_f in cond.items():
                            ex = _get_contract_extion_from_dict(
                                cond_f, f, varinfo, tag, sys_state, *args, **kw)
                            if ex is not None:
                                raise ex

                for varinfo, cond_f in cond_opts.items():
                    ex = _get_contract_extion_from_dict(
                        cond_f, f, varinfo, tag, sys_state, *args, **kw)
                    if ex is not None:
                        raise ex

            return f(*args, **kw)

        return wrapped

    return _in_contract


def out_contract(
        cond_f: Callable[..., bool],
        tag: Optional[str] = None,
        sys_state: ContractState = SYS_STATE):

    def _out_contract(f: Callable):

        @functools.wraps(f)
        def wrapped(*args, **kw):
            result = f(*args, **kw)
            if sys_state.is_enable and not cond_f(result):
                raise _new_contract_exception(cond_f, tag, result)
            return result

        return wrapped

    return _out_contract
