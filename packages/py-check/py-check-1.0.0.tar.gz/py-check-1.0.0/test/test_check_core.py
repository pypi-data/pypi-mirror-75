import math
import pytest
from pycheck import check


def func():
    return 1


test_cases = [('integer_case', 1), ('integer_case', int(2.1)),
              ('float_case', 0.2), ('float_case', math.inf),
              ('boolean_case', True), ('boolean_case', False),
              ('string_case', ''), ('string_case', 'str'), ('list_case', []),
              ('list_case', [1, 2, 3]), ('list_case', ['a', 'b']),
              ('dictionary_case', dict()), ('dictionary_case', dict({'a': 1})),
              ('dictionary_case', dict({'b': 2})), ('set_case', set()),
              ('set_case', {1, 'a'}), ('tuple_case', tuple()),
              ('tuple_case', tuple((1, 2))), ('tuple_case', (2, 3)),
              ('none_case', None), ('function_case', func)]

checker_list = [
    check.integer, check.float, check.boolean, check.string, check.list,
    check.dictionary, check.set, check.tuple, check.none
]


def value_ids(fixture_value):
    return f'{fixture_value[0]}-{fixture_value[1]}'


def checker_ids(fixture_value):
    return f'{fixture_value.__name__}_checker'


@pytest.mark.parametrize('value', test_cases, ids=value_ids)
def test_integer_checker(value):
    if value[0] == 'integer_case':
        assert check.integer(value[1]) == True
    else:
        assert check.integer(value[1]) == False


@pytest.mark.parametrize('value', test_cases, ids=value_ids)
def test_float_checker(value):
    if value[0] == 'float_case':
        assert check.float(value[1]) == True
    else:
        assert check.float(value[1]) == False


@pytest.mark.parametrize('value', test_cases, ids=value_ids)
def test_boolean_checker(value):
    if value[0] == 'boolean_case':
        assert check.boolean(value[1]) == True
    else:
        assert check.boolean(value[1]) == False


@pytest.mark.parametrize('value', test_cases, ids=value_ids)
def test_string_checker(value):
    if value[0] == 'string_case':
        assert check.string(value[1]) == True
    else:
        assert check.string(value[1]) == False


@pytest.mark.parametrize('value', test_cases, ids=value_ids)
def test_list_checker(value):
    if value[0] == 'list_case':
        assert check.list(value[1]) == True
    else:
        assert check.list(value[1]) == False


@pytest.mark.parametrize('value', test_cases, ids=value_ids)
def test_dictionary_checker(value):
    if value[0] == 'dictionary_case':
        assert check.dictionary(value[1]) == True
    else:
        assert check.dictionary(value[1]) == False


@pytest.mark.parametrize('value', test_cases, ids=value_ids)
def test_set_checker(value):
    if value[0] == 'set_case':
        assert check.set(value[1]) == True
    else:
        assert check.set(value[1]) == False


@pytest.mark.parametrize('value', test_cases, ids=value_ids)
def test_tuple_checker(value):
    if value[0] == 'tuple_case':
        assert check.tuple(value[1]) == True
    else:
        assert check.tuple(value[1]) == False


@pytest.mark.parametrize('value', test_cases, ids=value_ids)
def test_none_checker(value):
    if value[0] == 'none_case':
        assert check.none(value[1]) == True
    else:
        assert check.none(value[1]) == False


@pytest.mark.parametrize('value', test_cases, ids=value_ids)
def test_function_checker(value):
    if value[0] == 'function_case':
        assert check.function(value[1]) == True
    else:
        assert check.function(value[1]) == False


@pytest.mark.parametrize('checker_func', checker_list, ids=checker_ids)
def test_checker_with_empty_argument(checker_func):
    with pytest.raises(TypeError) as err:
        checker_func()

    assert 'missing 1 required positional argument' in str(err.value)


@pytest.mark.parametrize('checker_func', checker_list, ids=checker_ids)
def test_checker_with_multiple_arguments(checker_func):
    with pytest.raises(TypeError) as err:
        checker_func(1, 2, 3)

    assert 'takes 1 positional argument but 3 were given' in str(err.value)
