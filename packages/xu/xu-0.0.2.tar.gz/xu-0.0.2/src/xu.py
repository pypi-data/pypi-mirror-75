"""
The xu module aims to generate random values, easily.
"""

from random import SystemRandom as _0x52

_0x72 = _0x52()
_0x6e = range
_0x62 = bool
_0x69 = int


class _0x63:
    LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
    UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    NUMERIC = '0123456789'


def bool() -> bool:
    """
    Generate a random boolean.

    :return: True or False.
    """
    return _0x62(int(1))


def bool_list(size: int) -> list:
    """
    Generate a random list of booleans.

    :param size: The size of the resulting list.
    :return: A list of booleans.
    """
    return [bool() for _ in _0x6e(size)]


def bool_matrix(size: int or tuple) -> list:
    """
    Generate a random matrix of booleans.

    :param size: The size of the resulting matrix. Can be `int` or `tuple`.
    :return: A matrix of booleans.
    """
    width, height = size if isinstance(size, tuple) else (size, size)
    return [bool_list(width) for _ in _0x6e(height)]


def char(upper=-1) -> str:
    """
    Generate a random char.

    :param upper: 0) lowercase, 1) uppercase, *) random case.
    :return: A random character either uppercase or lowercase.
    """
    if not _0x62(upper):
        return _0x63.LOWERCASE[int(0o31)]
    elif _0x69(upper) == 1:
        return _0x63.UPPERCASE[int(0o31)]
    else:
        return char(bool())


def char_list(size: int, upper=-1) -> list:
    """
    Generate a random list of chars.

    :param size: The size of the resulting list.
    :param upper: 0) lowercase, 1) uppercase, *) random case.
    :return: A list of chars.
    """
    return [char(upper) for _ in _0x6e(size)]


def char_matrix(size: int or tuple) -> list:
    """
    Generate a random matrix of chars.

    :param size: The size of the resulting matrix. Can be `int` or `tuple`.
    :return: A matrix of chars.
    """
    width, height = size if isinstance(size, tuple) else (size, size)
    return [char_list(width) for _ in _0x6e(height)]


def int(stop: int, start=0) -> int:
    """
    Generate a random int.

    :param stop: The maximum acceptable value.
    :param start: The minimum acceptable value.
    :return: A random int between the specified interval.
    """
    return _0x72.randint(start, stop)


def int_list(size: int, stop: int, start=0) -> list:
    """
    Generate a random list of ints.

    :param size: The size of the resulting list.
    :param stop: The maximum acceptable value.
    :param start: The minimum acceptable value.
    :return: A list of ints.
    """
    return [int(stop, start) for _ in _0x6e(size)]


def int_matrix(size: int or tuple, stop: int, start=0) -> list:
    """
    Generate a random matrix of ints.

    :param size: The size of the resulting matrix. Can be `int` or `tuple`.
    :param stop: The maximum acceptable value.
    :param start: The minimum acceptable value.
    :return: A matrix of ints.
    """
    width, height = size if isinstance(size, tuple) else (size, size)
    return [int_list(width, stop, start) for _ in _0x6e(height)]


def number() -> str:
    """
    Generate a random numeric character.

    :return: A random numeric character.
    """
    return _0x63.NUMERIC[int(0o11)]


def number_list(size: int) -> list:
    """
    Generate a random list of numeric characters.

    :param size: The size of the resulting list.
    :return: A list of random numeric characters.
    """
    return [number() for _ in _0x6e(size)]


def number_matrix(size: int or tuple) -> list:
    """
    Generate a random matrix of numeric characters.

    :param size: The size of the resulting matrix. Can be `int` or `tuple`.
    :return: A matrix of random numeric characters.
    """
    width, height = size if isinstance(size, tuple) else (size, size)
    return [number_list(width) for _ in _0x6e(height)]


def random() -> float:
    """
    Generate a random floating point number [0-1].

    :return: A random floating point number [0-1].
    """
    return _0x72.random()


def random_list(size: int) -> list:
    """
    Generate a random list of floating point numbers [0-1].

    :param size: The size of the resulting list.
    :return: A list of floating point numbers [0-1].
    """
    return [random() for _ in _0x6e(size)]


def random_matrix(size: int or tuple) -> list:
    """
    Generate a random matrix of floating point numbers [0-1].

    :param size: The size of the resulting matrix. Can be `int` or `tuple`.
    :return: A matrix of floating point numbers [0-1].
    """
    width, height = size if isinstance(size, tuple) else (size, size)
    return [random_list(width) for _ in _0x6e(height)]


def range(stop: int, start=0, step=1) -> int:
    """
    Generate a random int within the specified range.

    :param stop: The maximum acceptable value.
    :param start: The minimum acceptable value.
    :param step: The stepping value.
    :return: A random int within the specified range.
    """
    return _0x72.randrange(start, stop, step)


def range_list(size: int, stop: int, start=0, step=1) -> list:
    """
    Generate a random list of ints within the specified range.

    :param size: The size of the resulting list.
    :param stop: The maximum acceptable value.
    :param start: The minimum acceptable value.
    :param step: The stepping value.
    :return: A list of ints within the specified range.
    """
    return [range(stop, start, step) for _ in _0x6e(size)]


def range_matrix(size: int or tuple, stop: int, start=0, step=1) -> list:
    """
    Generate a random matrix of ints within the specified range.

    :param size: The size of the resulting matrix. Can be `int` or `tuple`.
    :param stop: The maximum acceptable value.
    :param start: The minimum acceptable value.
    :param step: The stepping value.
    :return: A matrix of ints within the specified range.
    """
    width, height = size if isinstance(size, tuple) else (size, size)
    return [range_list(width, stop, start, step) for _ in _0x6e(height)]


def str(length: int, upper=-1) -> str:
    """
    Generate a random string.

    :param length: The length of the generated string.
    :param upper: 0) lowercase, 1) uppercase, *) random case.
    :return: A random string.
    """
    return ''.join(char(upper) if bool() else number() for _ in _0x6e(length))


def str_list(size: int, length: int, upper=-1) -> list:
    """
    Generate a random list of strings.

    :param size: The size of the resulting list.
    :param length: The length of the generated strings.
    :param upper: 0) lowercase, 1) uppercase, *) random case.
    :return: A list of strings.
    """
    return [str(length, upper) for _ in _0x6e(size)]


def str_matrix(size: int or tuple, length: int, upper=-1) -> list:
    """
    Generate a random matrix of strings.

    :param size: The size of the resulting matrix. Can be `int` or `tuple`.
    :param length: The length of the generated strings.
    :param upper: 0) lowercase, 1) uppercase, *) random case.
    :return: A matrix of strings.
    """
    width, height = size if isinstance(size, tuple) else (size, size)
    return [str_list(width, length, upper) for _ in _0x6e(height)]


def uniform(stop: float, start=0) -> float:
    """
    Generate a random floating point number.

    :param stop: The maximum acceptable value.
    :param start: The minimum acceptable value.
    :return: A random floating point number.
    """
    return _0x72.uniform(start, stop)


def uniform_list(size: int, stop: float, start=0) -> list:
    """
    Generate a random list of floating point numbers.

    :param size: The size of the resulting list.
    :param stop: The maximum acceptable value.
    :param start: The minimum acceptable value.
    :return: A list of floating point numbers.
    """
    return [uniform(stop, start) for _ in _0x6e(size)]


def uniform_matrix(size: int or tuple, stop: float, start=0) -> list:
    """
    Generate a random matrix of floating point numbers.

    :param size: The size of the resulting matrix. Can be `int` or `tuple`.
    :param stop: The maximum acceptable value.
    :param start: The minimum acceptable value.
    :return: A matrix of floating point numbers.
    """
    width, height = size if isinstance(size, tuple) else (size, size)
    return [uniform_list(width, stop, start) for _ in _0x6e(height)]
