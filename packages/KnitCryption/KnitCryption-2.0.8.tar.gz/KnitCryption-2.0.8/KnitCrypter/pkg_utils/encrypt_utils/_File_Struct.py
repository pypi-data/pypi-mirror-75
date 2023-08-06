from ._Needle_Struct import _Stitch_Struct as _S, _Unknit_Struct as _U


def _retrieve_contents(path, encoding):
    temp_read = open(path, mode='r', encoding=encoding)
    contents = temp_read.readlines()
    temp_read.close()
    return contents


def _prepare_file_to_modify(path, encoding):
    return open(path, mode='w', encoding=encoding)


class _File_Struct:

    def __init__(self, path, pattern, encoding):
        self.__contents = _retrieve_contents(path, encoding)
        self.__opened_file = _prepare_file_to_modify(path, encoding)
        self.__pattern = pattern

    @property
    def contents(self):
        return self.__contents

    def stitch(self, **kwargs):
        return _S(self, pattern=self.__pattern, contents=self.contents)

    def unknit(self, **kwargs):
        return _U(self, pattern=self.__pattern, contents=self.contents)

    def close(self):
        self.__opened_file.writelines(self.__contents)
        self.__opened_file.close()
