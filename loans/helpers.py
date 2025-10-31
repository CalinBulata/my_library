import math

def is_prime(number):
    if not isinstance(number, int):
        raise ValueError("Input must be an integer.")

    if number <= 1:
        return False

    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False

    return True