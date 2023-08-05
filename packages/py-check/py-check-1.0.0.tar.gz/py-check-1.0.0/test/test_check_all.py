import pytest
from pycheck import check

checker_list = [
    check.all.integer, check.all.float, check.all.boolean, check.all.string,
    check.all.list, check.all.dictionary, check.all.set, check.all.tuple
]


def checker_ids(fixture_value):

    return f'all_{fixture_value.__name__}_checker'


class TestAllIntegerChecker:
    def test_integer_case(self):
        assert check.all.integer(1) == True

    def test_integer_list_case(self):
        assert check.all.integer([1, 2, 3]) == True

    def test_integer_arguments_case(self):
        assert check.all.integer(1, 2, 3) == True

    def test_partial_integer_list_case(self):
        assert check.all.integer([1, 2, 1.1]) == False

    def test_partial_integer_arguments_case(self):
        assert check.all.integer(1, 2, 1.1) == False


@pytest.mark.parametrize('checker_func', checker_list, ids=checker_ids)
def test_all_checker_with_empty_argument(checker_func):
    with pytest.raises(TypeError) as err:
        checker_func()

    assert 'needs at least 1 argument' in str(err.value)


@pytest.mark.parametrize('checker_func', checker_list, ids=checker_ids)
def test_all_checker_with_only_keyword_argument(checker_func):
    with pytest.raises(TypeError) as err:
        checker_func(k=1)

    assert 'needs at least 1 argument' in str(err.value)


@pytest.mark.parametrize('checker_func', checker_list, ids=checker_ids)
def test_all_checker_with_position_argument_and_keyword_argument(checker_func):
    with pytest.raises(TypeError) as err:
        checker_func(1, k=1)

    assert 'got an unexpected keyword argument' in str(err.value)
