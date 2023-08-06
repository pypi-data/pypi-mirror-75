from KnitCrypter.pkg_utils._Assignment_Handler import _Assignment_Handler
from KnitCrypter.pkg_utils._Context_Manager import _Context_Manager
from KnitCrypter.pkg_utils.encrypt_utils.error_checks import _Encrypt_Errors

__version__ = [2, 0, 8]
__all__ = ["_Encrypt_Errors", "knitpattern", "knitcrypt"]


def default(a):
    return a


def equals(a, b):
    if a % b == 0:
        return a
    return a * -1


def notequals(a, b):
    if a % b != 0:
        return a
    return a * -1


class knitpattern(_Assignment_Handler):

    def __init__(self, string, base, func=default, *args, **kwargs):
        super().__init__(string, base, func, *args, **kwargs)


class knitcrypt(_Context_Manager):

    def __init__(self, path, pattern: knitpattern, **kwargs):
        super().__init__(path, pattern, **kwargs)
