from pycheck.check_utils import rename_function


def func():
    return 1


def test_rename_function():
    renamed_func = rename_function(func, 'new_func')
    assert renamed_func.__name__ == 'new_func'  # pylint: disable=no-member
