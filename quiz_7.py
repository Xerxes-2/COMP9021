from math import sqrt


def centrifuge(n, k):
    if k == 0 or n == k:
        return True
    r = n - k
    prime_factor = []
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            while n % i == 0:
                n //= i
            prime_factor.append(i)
    if n != 1 and n != r + k:
        prime_factor.append(n)
    if not prime_factor:
        return False
    return check_sum(prime_factor, k) and check_sum(prime_factor, r)


def check_sum(factors, goal):
    if goal == 0:
        return True
    if not factors:
        return False
    new_factors = factors[:-1]
    for j in range(0, goal + 1, factors[-1]):
        if check_sum(new_factors, goal - j):
            return True
    else:
        return False
