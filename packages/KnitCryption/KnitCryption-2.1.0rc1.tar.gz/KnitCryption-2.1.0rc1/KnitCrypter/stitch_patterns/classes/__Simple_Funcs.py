def Default(step: int):
    """
    Default return expression. Returns the step passed into it.
    """
    return step


def PowerOf(step: int, exponent: int):
    """
    Returns the given step multiplied to the power of the exponent.
    """
    return step**exponent


def Square(step: int):
    """
    Returns the square of the given step.
    """
    return step**2


def Cube(step: int):
    """
    Returns the cube of the given step.
    """
    return step**3


def Offset(step: int, offset: int):
    """
    Returns the given step modified by a given offset integer.
    """
    return step + offset
