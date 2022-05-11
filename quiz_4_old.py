# Written by Shupeng Xue for COMP9021
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
    """list of primes up to n"""
    sieve = [True] * (n + 1)
    for p in range(2, round(sqrt(n)) + 1):
        if sieve[p]:
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return sieve


def tri_numbers(n):
    """Output: the number of trinumbers at most equal to nn included...blabla"""
    sieve = sieve_of_primes_up_to(int(n/4)+1)
    sieve_list = [i for i in range(2, int(n/4)+2) if sieve[i]]
    trinumbers = set()
    for i in sieve_list:
        for j in sieve_list:
            if (2*i*j > n) | (j > i):
                break
            for k in sieve_list:
                if (j*i*k > n) | (k > j):
                    break
                trinumbers.add((i*j*k, k, j, i, min(i-j, j-k)))
    tri_list = sorted(trinumbers)
    numb = len(trinumbers)
    if numb == 1:
        print('There is ', numb, ' trinumber at most equal to ', n, '.', sep='')
    else:
        print('There are ', numb, ' trinumbers at most equal to ', n, '.', sep='')
    print('The largest one is ', tri_list[-1][0],
          ', equal to ', tri_list[-1][1], ' x ', tri_list[-1][2],
          ' x ', tri_list[-1][3], '.', sep='')
    print()
    gap = sorted(trinumbers, key=lambda t: t[4], reverse=True)
    print('The maximum gap in decompositions is ', gap[0][4], '.', sep='')
    print('It is achieved with:')
    max_gap = []
    for t in gap:
        if t[4] == gap[0][4]:
            max_gap.append(t)
        else:
            break
    output = sorted(max_gap, key=lambda t: t[0])
    for t in output:
        print('  ', t[0], ' = ', t[1], ' x ', t[2],
              ' x ', t[3], sep='')

