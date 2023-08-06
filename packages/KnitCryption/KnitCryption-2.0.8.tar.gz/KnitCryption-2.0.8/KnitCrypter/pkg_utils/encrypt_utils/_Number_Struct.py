from .error_checks._Encrypt_Cases import _verify_and_set_base
from .error_checks._Encrypt_Cases import _verify_attribute_set
from .error_checks._Encrypt_Cases import _verify_value_gt_zero
from .error_checks._Encrypt_Cases import _base_is_integer_value
from re import findall


class _Number_Struct:

    """
    Converts a number into the desired format

    supported formats:
        - hex     '0x'
        - oct     '0o'
        - int     '00'
        - 2-10    '0b'
    """

    def __init__(self, initial_value, base_value):
        super().__init__()
        self._base_value = base_value
        self._value = initial_value

    def __repr__(self):
        return str(self._value)

    def __str__(self):
        return str(self._value)

    @property
    def _base_value(self):
        return self.__base_value

    @property
    def _value(self):
        return self.__value

    @_base_value.setter
    def _base_value(self, new_base: int or hex or oct):
        _verify_attribute_set(self, "__base_value")
        if _base_is_integer_value(new_base):
            self.__base_value = _verify_and_set_base(new_base)
        else:
            self.__base_value = new_base

    @_value.setter
    def _value(self, new_value: int):
        _verify_attribute_set(self, "__value")
        self.__value = _convert_value(self, new_value)


def _convert_value(n: _Number_Struct, value):
    value = _Convert._into[int](value)
    try:
        return _Convert._into[n._base_value](value)
    except KeyError:
        return _into_base(value, n._base_value)


def _into_hex(init_value: int):
    return hex(init_value)


def _into_oct(init_value: int):
    return oct(init_value)


def _into_int(init_value: int):
    _extracted_id = _extract_base_id(init_value)
    return _Convert._from[_extracted_id](init_value)


def _into_base(init_value: int, base: int):
    new_value = "".join(_get_new_digits(init_value, base))
    return f"{base}b{new_value}"


def _from_hex(value: hex):
    return int(value, base=16)


def _from_oct(value: oct):
    return int(value, base=8)


def _from_int(value: int):
    return value


def _from_base(value: str):
    return int(_extract_value(value), base=_extract_base_value(value))


def _extract_base_id(value):
    try:
        return '0'+findall(r"[xob]", value)[0]
    except TypeError:
        return '00'


def _extract_base_value(value):
    return int(findall(r"(\d+)b", value)[0])


def _extract_value(value):
    return findall(r"b(\d+)", value)[0]


def _get_new_digits(value: int, base: int):
    remainder_stack = _verify_value_gt_zero(value)
    while value > 0:
        remainder_stack.insert(0, _get_remainder(value, base))
        value //= base
    return remainder_stack


def _get_remainder(value: int, modulo: int):
    return str(value % modulo)


class _Convert:

    _into = {
        int: _into_int,
        hex: _into_hex,
        oct: _into_oct
    }

    _from = {
        "0x": _from_hex,
        "0o": _from_oct,
        "0b": _from_base,
        "00": _from_int
    }
