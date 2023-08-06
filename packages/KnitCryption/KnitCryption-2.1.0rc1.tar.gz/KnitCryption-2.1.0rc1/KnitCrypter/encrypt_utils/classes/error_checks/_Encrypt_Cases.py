from ._Encrypt_Errors import SequenceError
from os.path import exists


def _extract_type(o: object):
    return str(o.__class__).strip(" <clas>")


def _verify_value_gt_zero(value: int):
    if value > 0:
        return []
    return '0'


def _base_is_integer_value(desired_base):
    return desired_base == int and type(desired_base) != type


def _verify_and_set_base(base: int):
    if base in range(2, 11):
        return base
    raise ValueError(f"Base '{base}' not within inclusive range 2-10")


def _verify_char_value(char):
    type_name = _extract_type(char)
    if type(char) != str or len(char) > 1:
        raise TypeError(f"expected 'char' not '{type_name}'")


def _verify_attribute_set(o: object, attribute):
    if o.__dict__.__contains__(attribute):
        attr_name = attribute.strip("_")
        raise AttributeError(f"attribute '{attr_name}' has already been set")


def _separate_keys_from_values(pattern: dict):
    return list(pattern.keys()), list(pattern.values())


def _compare_sequence_attributes(i, pattern: dict):
    sequence = _separate_keys_from_values(pattern)
    for j in range(len(pattern)):
        if sequence[0][i] == sequence[0][j] and i != j:
            raise SequenceError(pattern, 1)
        if sequence[1][i] == sequence[1][j] and i != j:
            raise SequenceError(pattern, 0)


def _verify_sequence_pattern(pattern: dict):
    for i in range(len(pattern)):
        _compare_sequence_attributes(i, pattern)


def _verify_file_exists(file_path: str):
    if not exists(file_path):
        raise FileNotFoundError(f"file '{file_path}' is does not exist")


def _verify_file_encrypted(file_lines: list, file_encrypted_stamp: str):
    return file_lines[-1] == file_encrypted_stamp


def _verify_mode_flags(o: object, flag):
    if not o._mode_flags.__contains__(flag):
        raise AttributeError(f"flag '{flag}' does not exist as a legal flag")
