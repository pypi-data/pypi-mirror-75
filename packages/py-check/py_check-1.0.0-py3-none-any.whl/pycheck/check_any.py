from pycheck.check_core import CheckCore
from pycheck.check_utils import get_all_function_from_class, rename_function, get_function_arguments, validate_func_args_kwargs


def any_method(func):
    def any_method_wrapper(*args, **kwargs):
        validate_func_args_kwargs(func.__name__, args, kwargs)
        arguments = get_function_arguments(args)
        for argument in arguments:
            if func(argument, **kwargs):
                return True
        return False

    return rename_function(any_method_wrapper, func.__name__)


class CheckAny:
    pass


for function_tuple in get_all_function_from_class(CheckCore):
    function_name, function = function_tuple
    if 'any' in function.__dict__.get('interface'):
        setattr(CheckAny, function_name, staticmethod(any_method(function)))
