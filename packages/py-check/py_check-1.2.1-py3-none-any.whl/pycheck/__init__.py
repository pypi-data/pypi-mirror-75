from pycheck.check_core import CheckCore
from pycheck.check_all import CheckAll
from pycheck.check_any import CheckAny

name = 'py-check'

__all__ = ['check']


class Check(CheckCore):
    all: CheckAll = CheckAll
    any: CheckAny = CheckAny


check = Check
