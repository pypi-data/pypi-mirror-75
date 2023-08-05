import pytest
from pycheck import check

checker_list = [
    check.any.integer, check.any.float, check.any.boolean, check.any.string,
    check.any.list, check.any.dictionary, check.any.set, check.any.tuple
]


def checker_ids(fixture_value):

    return f'any_{fixture_value.__name__}_checker'


class TestAnyIntegerChecker:
    def test_integer_case(self):
        assert check.any.integer(1) == True

    def test_integer_list_case(self):
        assert check.any.integer([1, 2, 3]) == True

    def test_integer_arguments_case(self):
        assert check.any.integer(1, 2, 3) == True

    def test_partial_integer_list_case(self):
        assert check.any.integer([1, 2, 1.1]) == True

    def test_partial_integer_arguments_case(self):
        assert check.any.integer(1, 2, 1.1) == True

    def test_non_integer_list_case(self):
        assert check.any.integer(['a', 1.1, [1, 2]]) == False

    def test_non_integer_arguments_case(self):
        assert check.any.integer('a', 1.1, [1, 2]) == False


@pytest.mark.parametrize('checker_func', checker_list, ids=checker_ids)
def test_any_checker_with_empty_argument(checker_func):
    with pytest.raises(TypeError) as err:
        checker_func()

    assert 'needs at least 1 argument' in str(err.value)


@pytest.mark.parametrize('checker_func', checker_list, ids=checker_ids)
def test_any_checker_with_only_keyword_argument(checker_func):
    with pytest.raises(TypeError) as err:
        checker_func(k=2)

    assert 'needs at least 1 argument' in str(err.value)


@pytest.mark.parametrize('checker_func', checker_list, ids=checker_ids)
def test_any_checker_with_position_argument_and_keyword_argument(checker_func):
    with pytest.raises(TypeError) as err:
        checker_func(1, k=2)

    assert 'got an unexpected keyword argument' in str(err.value)
