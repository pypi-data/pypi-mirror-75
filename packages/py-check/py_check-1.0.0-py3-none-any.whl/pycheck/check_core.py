from typing import Any


def test():
    print(123)


class CheckCore:
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


# Set check function interface
CheckCore.integer.interface = ['all', 'any']
CheckCore.float.interface = ['all', 'any']
CheckCore.boolean.interface = ['all', 'any']
CheckCore.string.interface = ['all', 'any']
CheckCore.list.interface = ['all', 'any']
CheckCore.dictionary.interface = ['all', 'any']
CheckCore.set.interface = ['all', 'any']
CheckCore.tuple.interface = ['all', 'any']
CheckCore.none.interface = ['all', 'any']
CheckCore.function.interface = ['all', 'any']
