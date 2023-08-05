from sys import version_info
from typing import TypeVar, List, Tuple, Any, Dict
from types import FunctionType

T = TypeVar('T')


def get_all_function_from_class(cls) -> List[Tuple[str, FunctionType]]:
    function_list = [
        func_name for func_name in dir(cls)
        if (not func_name.startswith('__')) and (not func_name.endswith('__'))
    ]
    return [(func_name, getattr(cls, func_name))
            for func_name in function_list]


def rename_function(func: T, new_name: str) -> T:
    code_object = func.__code__
    function, code = type(func), type(code_object)
    if version_info >= (3, 8):
        return function(
            code(code_object.co_argcount, code_object.co_posonlyargcount,
                 code_object.co_kwonlyargcount, code_object.co_nlocals,
                 code_object.co_stacksize, code_object.co_flags,
                 code_object.co_code, code_object.co_consts,
                 code_object.co_names, code_object.co_varnames,
                 code_object.co_filename, new_name, code_object.co_firstlineno,
                 code_object.co_lnotab, code_object.co_freevars,
                 code_object.co_cellvars), func.__globals__, new_name,
            func.__defaults__, func.__closure__)

    return function(
        code(code_object.co_argcount, code_object.co_kwonlyargcount,
             code_object.co_nlocals, code_object.co_stacksize,
             code_object.co_flags, code_object.co_code, code_object.co_consts,
             code_object.co_names, code_object.co_varnames,
             code_object.co_filename, new_name, code_object.co_firstlineno,
             code_object.co_lnotab, code_object.co_freevars,
             code_object.co_cellvars), func.__globals__, new_name,
        func.__defaults__, func.__closure__)


def get_function_arguments(args: Tuple[Any, ...]) -> List[Any]:
    if len(args) == 1 and isinstance(args[0], list):
        return args[0]
    return list(args)


def validate_func_args_kwargs(func_name: str, args: Tuple[Any, ...],
                              kwargs: Dict[str, any]):
    if len(args) == 0:
        raise TypeError(f'{func_name}() needs at least 1 argument')
    if func_name != 'date_string' and len(kwargs) > 0:
        raise TypeError(
            f'{func_name}() got an unexpected keyword argument \'{next(iter(kwargs))}\''
        )
