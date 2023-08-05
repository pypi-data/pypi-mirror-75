"""Main module."""


def add(x: int, y: int) -> int:
    """

    @return:
    @return:
    @param x:
    @param y:
    @return:
    """
    return x + y


def factorial(x: int) -> int:
    """
    factorial

    @param x: input value
    @return: facial value
    """
    initial = 1

    for i in range(1, x+1):
        initial *= i

    return initial


def permutation(x: int, y: int) -> int:
    """

    @param x:  numerator
    @param y: denominator
    @return: comnination value
    """
    return int(factorial(x) / factorial(y))


def combination(x: int, y: int) -> int:
    """

    @param x:  numerator
    @param y: denominator
    @return: comnination value
    """
    return int(factorial(x) / (factorial(y) * factorial(x-y)))

