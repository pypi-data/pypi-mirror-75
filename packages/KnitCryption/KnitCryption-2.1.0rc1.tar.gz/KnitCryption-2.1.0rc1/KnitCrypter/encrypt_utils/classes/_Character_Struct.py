from .error_checks._Encrypt_Cases import _verify_attribute_set
from .error_checks._Encrypt_Cases import _verify_char_value


class _Character_Struct:

    """
    Represents a single character

    e.g. 'h' not 'ha'
    """

    def __init__(self, char: str):
        self._char = char

    def __repr__(self):
        return f"{self._char}"

    @property
    def _char(self):
        return self.__char

    @_char.setter
    def _char(self, char: str):
        _verify_attribute_set(self, '__char')
        _verify_char_value(char)
        self.__char = char
