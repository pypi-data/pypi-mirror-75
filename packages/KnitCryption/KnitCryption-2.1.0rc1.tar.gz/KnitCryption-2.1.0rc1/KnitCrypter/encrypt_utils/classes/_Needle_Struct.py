from .error_checks._Encrypt_Cases import _verify_file_encrypted
from .error_checks._Encrypt_Errors import EncryptionError
from abc import ABCMeta, abstractmethod

ENCRYPTED = '###_________#FILE_ENCRYPTED#_________###'


def _split_tied_string(pattern, string):
    string = string.strip('\n')
    string = string.split(pattern.prefix)[1:]
    return [pattern.prefix+c for c in string]


def _untie_chars(pattern, array: [str]):
    return [pattern.sequence.from_values[c] for c in array]


def _stitch_chars(pattern, array: [str]):
    return [pattern.sequence.from_keys[c] for c in array]


def _stitch_string(o: object, string: str) -> str:
    return "".join(_stitch_chars(o._pattern, [c for c in string]))


def _untie_string(o: object, string: str):
    split_string = _split_tied_string(o._pattern, string)
    return "".join(_untie_chars(o._pattern, split_string))


class _Needle_Struct(metaclass=ABCMeta):

    def __init__(self, super_obj, pattern, contents):
        self._super_obj = super_obj
        self._pattern = pattern
        self._contents = contents
        self._is_encrypted = _verify_file_encrypted(self._contents, ENCRYPTED)

    def __del__(self):
        self._super_obj.__contents = self._contents

    @abstractmethod
    def all_lines(self):
        raise NotImplementedError

    @abstractmethod
    def from_lines(self, *args):
        raise NotImplementedError

    def stamp_contents(self):
        self._contents.append('\n'+ENCRYPTED)

    def erase_stamp(self):
        if self._contents[-1] == ENCRYPTED:
            self._contents.pop(-1)


class _Stitch_Struct(_Needle_Struct):

    def all_lines(self):
        if self._is_encrypted:
            raise EncryptionError('file already encrypted, cannot continue')
        for i in range(len(self._contents)):
            self._contents[i] = _stitch_string(self, self._contents[i])

    def from_lines(self, *args):
        if len(args) > 2:
            raise AttributeError("'from_lines' accepts only 2 arguments")


class _Unknit_Struct(_Needle_Struct):

    def all_lines(self):
        if not self._is_encrypted:
            raise EncryptionError('file not encrypted, cannot continue')
        for i in range(len(self._contents)):
            self._contents[i] = _untie_string(self, self._contents[i])

    def from_lines(self, *args):
        if len(args) > 2:
            raise AttributeError("'from_lines' accepts only 2 arguments")
