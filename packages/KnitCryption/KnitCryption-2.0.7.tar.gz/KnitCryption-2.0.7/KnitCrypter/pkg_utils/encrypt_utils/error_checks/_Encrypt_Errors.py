def _extract_type(o: object):
    return str(o.__class__).strip(" <clas>")


class SequenceError(Exception):

    _error_reasons = {
        0: lambda array: f"{array} has one or more equivalent values",
        1: lambda array: f"{array} has one or more equivalent keys"
    }

    def __init__(self, array, reason=0):
        array = _extract_type(array)
        self._reason = self._error_reasons[reason](array)
        super().__init__()

    def __str__(self):
        return self._reason


class EncryptionError(Exception):

    def __init__(self, message="error occured trying to encrypt the file"):
        self._message = message
        super().__init__()

    def __str__(self):
        return self._message
