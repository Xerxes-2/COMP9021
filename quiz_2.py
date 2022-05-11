# Written by Shupeng Xue for COMP9021
#
# Implements three functions:
# - binary_lunar_addition(number_1, number_2)
#   that lunarly (or is it lunatically?) adds number_2 to number_1;
# - lunar_addition(*numbers)
#   that lunarly adds all arguments;
# - binary_lunar_multiplication(multiplicand, multiplier)
#   that lunarly multiplies multiplicand by multiplier.
#
# Both operations are discussed at
# https://www.youtube.com/watch?v=cZkGeR9CWbk
# Watch it!
#
# Essentially, lunar addition and lunar multiplication
# are like standard addition and multiplication, except that:
# - the lunar sum of two digits is the largest of both digits;
# - the lunar product of two digits is the smallest of both digits.
#
# You can assume that the function arguments are exactly as expected,
# namely, positive numbers (possibly equal to 0).


def binary_lunar_addition(number_1, number_2):
    result = 0
    str_1 = str(number_1)
    len_1 = len(str_1)
    str_2 = str(number_2)
    len_2 = len(str_2)
    min_len = min(len_1, len_2)
    str_result = ''
    for i in range(1, min_len+1):
        if int(str_1[-i]) <= int(str_2[-i]):
            str_result = str_2[-i]+str_result
        else:
            str_result = str_1[-i]+str_result
    if len_1 > len_2:
        str_result = str_1[0:-min_len]+str_result
    if len_1 < len_2:
        str_result = str_2[0:-min_len]+str_result
    result = int(str_result)
    return result


def lunar_addition(*numbers):
    result = 0
    for n in numbers:
        result = binary_lunar_addition(result, n)
    return result


def simple_mult(multiplicand, single):
    result = 0
    str_single = str(single)
    str_multiplicand = str(multiplicand)
    str_result = ''
    for char in str_multiplicand:
        if single >= int(char):
            str_result = str_result+char
        else:
            str_result = str_result+str_single
    result = int(str_result)
    return result


def binary_lunar_multiplication(multiplicand, multiplier):
    result = 0
    summer = ()
    str_multiplier = str(multiplier)
    len_multiplier = len(str_multiplier)
    for i in range(1, len_multiplier+1):
        summer = summer + \
            (pow(10, i-1)*simple_mult(multiplicand, int(str_multiplier[-i])),)
    result = lunar_addition(*summer)
    return result
