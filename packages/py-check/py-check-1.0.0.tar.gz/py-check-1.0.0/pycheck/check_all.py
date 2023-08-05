from pycheck.check_core import CheckCore
from pycheck.check_utils import get_all_function_from_class, rename_function, get_function_arguments, validate_func_args_kwargs


def all_method(func):
    def all_method_wrapper(*args, **kwargs):
        validate_func_args_kwargs(func.__name__, args, kwargs)
        arguments = get_function_arguments(args)
        for argument in arguments:
            if not func(argument, **kwargs):
                return False
        return True

    return rename_function(all_method_wrapper, func.__name__)


class CheckAll:
    pass


for function_tuple in get_all_function_from_class(CheckCore):
    function_name, function = function_tuple
    if 'all' in function.__dict__.get('interface'):
        setattr(CheckAll, function_name, staticmethod(all_method(function)))
