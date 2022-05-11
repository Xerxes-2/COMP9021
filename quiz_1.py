# Written by *** for COMP9021
#
# Prompts the user for two inputs, one of which is a
# random integer dim strictly greater than 2,
# and generates a list of random digits of length dim.
#
# Outputs some text and two "pictures".
# The text clarifies what "pictures" are expected.
#
# There are a few blank lines in the output,
# including one at the very end.


from random import seed, randrange
import sys


def border1(n):
    print('  ', '|', '-'*(2*n-1), '|', sep='')


def body1(n):
    print('  ', '|', ' '*(2*n-1), '|', sep='')
    print('  ', '|', ' '*(n-1), '*', ' '*(n-1), '|', sep='')
    print('  ', '|', ' '*(2*n-1), '|', sep='')


def border2(l):
    print('  ', '|', '-'.join(str(x) for x in l), '|', sep='')


def body2(n):
    print('  ', '|', ' '*(2*n-1), '|', sep='')
    print('  ', '|', ' '*(n - 2), '-'*3, ' '*(n-2), '|', sep='')
    print('  ', '|', ' '*(n - 2), '|*|', ' '*(n-2), '|', sep='')
    print('  ', '|', ' '*(n - 2), '-'*3, ' '*(n-2), '|', sep='')
    print('  ', '|', ' '*(2*n-1), '|', sep='')


try:
    for_seed, dim = (int(x) for x in input('Enter two integers, the second '
                                           'one being 3 or more: '
                                           ).split()
                     )
    if dim <= 2:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
digits = [randrange(10) for _ in range(dim)]
print()
print(f'The chosen dimension is {dim}.')
print(f'Also, I have this sequence of {dim} digits for you:')
print(' ', digits)
complement = [9-x for x in digits]
print()
print('Here is a first picture.')
print(f'There are {dim - 1} spaces on each side of the star.')
print()
border1(dim)
body1(dim)
border1(dim)
print()
print('Here is a second picture.')
print('Top and bottom borders are complementary, because:')
print(' ', '0 is 9\'s \"complement\".')
print(' ', '1 is 8\'s \"complement\".')
print(' ', '2 is 7\'s \"complement\".')
print(' ', '...')
print()
border2(digits)
body2(dim)
border2(complement)
print()
