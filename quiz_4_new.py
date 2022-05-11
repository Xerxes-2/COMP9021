# Written by Eric Martin for COMP9021
#
# Call "trinumber" any integer that is the product of
# 3 prime numbers, for instance:
# - 8, equal to 2 x 2 x 2
# - 363, equal to 3 x 11 x 11
# - 455, equal to 5 x 7 x 13
# - 231, equal to 3 x 7 x 11
# - 782, equal to 2 x 17 x 23
#
# Given a trinumber n, call "gap in its decomposition"
# the minimum of
# - the difference between second and first primes
#   in n's decomposition, and
# - the difference between third and second primes
#   in n's decomposition
# (ordering the 3 primes from smallest to largest).
# For instance,
# - the gap in the decomposition of 8 is 0 (2 - 2)
# - the gap in the decomposition of 363 is 0 (11 - 11)
# - the gap in the decomposition of 455 is 2 (7 - 5)
# - the gap in the decomposition of 231 is 4 (7 - 3 or 11 - 7)
# - the gap in the decomposition of 782 is 6 (23 - 17)
#
# Implements a function tri_numbers(n) that outputs:
# - the number of trinumbers at most equal to n included;
# - the largest trinumber at most equal to n included;
# - the maximum gap in the decomposition of trinumbers
#   at most equal to n included;
# - ordered from smallest to largest, the numbers having
#   that maximum gap in their decompositions,
#   together with their decompositions.
#
# You can assume that n is an integer at least equal to 8.
# In the tests, its value won't exceed 50_000_000.

from math import sqrt


def sieve_of_primes_up_to(n):
    sieve = [True] * (n + 1)
    for p in range(2, round(sqrt(n)) + 1):
        if sieve[p]:
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return sieve

def tri_numbers(n):
    sieve = sieve_of_primes_up_to(n // 4)
    primes = [i for i in range(2, n // 4 + 1) if sieve[i]]
    trinumbers = {}
    max_gap = -1
    upper_bound_1 = round(n ** (1 / 3))
    for i1 in range(len(primes)):
        prime_1 = primes[i1]
        if prime_1 > upper_bound_1:
            break
        upper_bound_2 = round(sqrt(n / prime_1))
        for i2 in range(i1, len(primes)):
            prime_2 = primes[i2]
            if prime_2 > upper_bound_2:
                break
            binumber = prime_1 * prime_2
            first_gap = prime_2 - prime_1
            upper_bound_3 = n // binumber
            for i3 in range(i2, len(primes)):
                prime_3 = primes[i3]
                if prime_3 > upper_bound_3:
                    break
                trinumber = binumber * prime_3
                trinumbers[trinumber] = prime_1, prime_2, prime_3
                gap = min(first_gap, prime_3 - prime_2)
                if gap > max_gap:
                    max_gap = gap
                    max_gap_solutions = [trinumber]
                elif gap == max_gap:
                    max_gap_solutions.append(trinumber)
    if len(trinumbers) == 1:
        print(f'There is 1 trinumber at most equal to {n}.')
    else:
        print(f'There are {len(trinumbers)} trinumbers at most equal to {n}.')
    max_trinumber = max(trinumbers)
    print(f'The largest one is {max_trinumber}, equal to',
          trinumbers[max_trinumber][0], 'x',
          trinumbers[max_trinumber][1], 'x',
          trinumbers[max_trinumber][2], end='.\n'
         )
    print()
    print(f'The maximum gap in decompositions is {max_gap}.')
    print('It is achieved with:')
    for trinumber in max_gap_solutions:
        print(' ', trinumber, '=',
              trinumbers[trinumber][0], 'x',
              trinumbers[trinumber][1], 'x',
              trinumbers[trinumber][2]
             )
