from sys import platform
from typing import Any
import datetime


class CheckCore:
    # Type checks
    # ----------------------------------------------------------------------
    @staticmethod
    def integer(value: Any) -> bool:
        """Checks if the given value type is integer.

        Parameters
        ----------
        value : Any
            Any input value.

        Returns
        -------
        bool
            True if input value is integer, False otherwise.
        """
        if isinstance(value, bool):
            return False
        return isinstance(value, int)

    @staticmethod
    def float(value: Any) -> bool:
        """Checks if the given value type is float.

        Parameters
        ----------
        value : Any
            Any input value.

        Returns
        -------
        bool
            True if input value is float, False otherwise.
        """
        return isinstance(value, float)

    @staticmethod
    def boolean(value: Any) -> bool:
        """Checks if the given value type is boolean.

        Parameters
        ----------
        value : Any
            Any input value.

        Returns
        -------
        bool
            True if input value is boolean, False otherwise.
        """
        return isinstance(value, bool)

    @staticmethod
    def string(value: Any) -> bool:
        """Checks if the given value type is string.

        Parameters
        ----------
        value : Any
            Any input value.

        Returns
        -------
        bool
            True if input value is string, False otherwise.
        """
        return isinstance(value, str)

    @staticmethod
    def char(value: Any) -> bool:
        """Checks if the given value type is string.

        Parameters
        ----------
        value : Any
            Any input value.

        Returns
        -------
        bool
            True if input value is string, False otherwise.
        """
        return isinstance(value, str) and len(value) == 1

    @staticmethod
    def list(value: Any) -> bool:
        """Checks if the given value type is list.

        Parameters
        ----------
        value : Any
            Any input value.

        Returns
        -------
        bool
            True if input value is list, False otherwise.
        """
        return isinstance(value, list)

    @staticmethod
    def dictionary(value: Any) -> bool:
        """Checks if the given value type is dictionary.

        Parameters
        ----------
        value : Any
            Any input value.

        Returns
        -------
        bool
            True if input value is dictionary, False otherwise.
        """
        return isinstance(value, dict)

    @staticmethod
    def set(value: Any) -> bool:
        """Checks if the given value type is set.

        Parameters
        ----------
        value : Any
            Any input value.

        Returns
        -------
        bool
            True if input value is set, False otherwise.
        """
        return isinstance(value, set)

    @staticmethod
    def tuple(value: Any) -> bool:
        """Checks if the given value type is tuple.

        Parameters
        ----------
        value : Any
            Any input value.

        Returns
        -------
        bool
            True if input value is tuple, False otherwise.
        """
        return isinstance(value, tuple)

    @staticmethod
    def none(value: Any) -> bool:
        """Checks if the given value type is None.

        Parameters
        ----------
        value : Any
            Any input value.

        Returns
        -------
        bool
            True if input value is None, False otherwise.
        """
        if value is None:
            return True
        return False

    @staticmethod
    def function(value: Any) -> bool:
        """Checks if the given value type is function.

        Parameters
        ----------
        value : Any
            Any input value.

        Returns
        -------
        bool
            True if input value is function, False otherwise.
        """
        return callable(value)

    @staticmethod
    def date(value: Any) -> bool:
        """Checks if the given value type is date.

        Parameters
        ----------
        value : Any
            Any input value.

        Returns
        -------
        bool
            True if input value is date, False otherwise.
        """
        return isinstance(value, datetime.date)

    @staticmethod
    def date_string(value: Any, string_pattern: str = '%Y-%m-%d') -> bool:
        """Checks if the given string type is date by string pattern.

        Parameters
        ----------
        value : Any
            Any input value.

        string_pattern : str
            Datetime format code string.
            Please see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
            for the detail of datetime format code.

        Returns
        -------
        bool
            True if input value is date which matches the pattern, False otherwise.
        """
        if isinstance(value, datetime.date):
            return True
        try:
            datetime.datetime.strptime(value, string_pattern)
        except (ValueError, TypeError):
            return False
        return True

    @staticmethod
    def same_type(value: Any, *args: Any) -> bool:
        """Checks if the given values type are the smae.

        Parameters
        ----------
        value : Any
            Any input value.

        args : Any
            Extra input values.
        Returns
        -------
        bool
            True if all input values are the same, False otherwise.
        """
        if len(args) == 0:
            return True
        target_type = type(value)
        for arg in args:
            # handle int value with bool value case
            if CheckCore.integer(value) and isinstance(arg, bool):
                return False
            if not isinstance(arg, target_type):
                return False
        return True

    # Environment checks
    # ----------------------------------------------------------------------
    @staticmethod
    def mac() -> bool:
        """Checks if current operating system is mac."""
        return platform == 'darwin'

    @staticmethod
    def windows() -> bool:
        """Checks if current operating system is windows."""
        return platform == 'win32'

    @staticmethod
    def linux() -> bool:
        """Checks if current operating system is linux."""
        return platform == 'linux'


# Set check function interface
CheckCore.integer.interface = ['all', 'any']
CheckCore.float.interface = ['all', 'any']
CheckCore.boolean.interface = ['all', 'any']
CheckCore.string.interface = ['all', 'any']
CheckCore.char.interface = ['all', 'any']
CheckCore.list.interface = ['all', 'any']
CheckCore.dictionary.interface = ['all', 'any']
CheckCore.set.interface = ['all', 'any']
CheckCore.tuple.interface = ['all', 'any']
CheckCore.none.interface = ['all', 'any']
CheckCore.function.interface = ['all', 'any']
CheckCore.date.interface = ['all', 'any']
CheckCore.date_string.interface = ['all', 'any']
