from math import inf


class __fibonacci_generator:

    __previous: int = 0
    __current: int = 1

    def __next__(self):
        return next(self.__generate_sequence())

    def __generate_sequence(self):
        while self.__previous < inf:
            self.__calculate()
            yield self.__current

    def __calculate(self):
        if self.__current < 1:
            self.__current += 1
            return None
        temp = self.__current
        self.__current += self.__previous
        self.__previous = temp


class __prime_generator:

    __held_number: int = 0

    def __next__(self):
        return next(self.__generate_sequence())

    def __generate_sequence(self):
        while self.__held_number < inf:
            self.__calculate()
            yield self.__held_number

    def __calculate(self):
        self.__held_number += 1
        while not self.__is_prime():
            self.__held_number += 1

    def __is_prime(self, test_value: int = 2):
        if test_value == self.__held_number or abs(self.__held_number) == 1:
            return True
        if self.__held_number % test_value != 0:
            return self.__is_prime(test_value+1)
        return False


def __fibonacci_calculator(step: int):
    fibonacci_sequence = __fibonacci_generator()
    for _ in range(step):
        next(fibonacci_sequence)
    return next(fibonacci_sequence)


def __prime_calculator(step: int):
    prime_sequence = __prime_generator()
    for _ in range(step):
        next(prime_sequence)
    return next(prime_sequence)


def __factorial_calulator(step: int, start: int):
    if step < 2:
        return step
    return step * __factorial_calulator(step - 1, start)


def Fibonacci(step: int):
    """
    Return an integer value based on the Fibonacci sequence from an index or a
    'step'.
    """
    return __fibonacci_calculator(step)


def Prime(step: int):
    """
    Return a prime integer base on the sequence of primes from an index or a
    'step'.
    """
    return __prime_calculator(step)


def Factorial(step: int):
    """
    Return the factorial of a given number in the form of a 'step'.
    """
    return __factorial_calulator(step, step)
