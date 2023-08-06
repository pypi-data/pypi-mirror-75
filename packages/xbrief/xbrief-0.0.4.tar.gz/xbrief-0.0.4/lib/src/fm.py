from borel import Zu, stat


#
# [format]
# format_spec     ::=  [[fill]align][sign][#][0][width][grouping_option][.precision][type]
# fill            ::=  <any character>
# align           ::=  "<" | ">" | "=" | "^"
# sign            ::=  "+" | "-" | " "
# width           ::=  digit+
# grouping_option ::=  "_" | ","
# precision       ::=  digit+
# type            ::=  "b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "X" | "%"
#
# [type]
# 'e' Exponent notation.
# 'f' Fixed-point notation.
# 'g' General format.
# 'n' Number.
# '%' Percentage.
# None, similar to 'g'
#


def max_len(numbers, digit=2, sep=True, is_pct=False):
    max_v, min_v = stat.bound(numbers)
    int_exp_max, int_exp_min = Zu.int_exponent(max_v), Zu.int_exponent(min_v)
    int_exp = max(int_exp_max, int_exp_min)
    if digit > 0:
        digit += 1
    if is_pct:
        int_exp += 2
    magni_sep = int(int_exp / 3) + 1 if sep else 0
    nega = 1 if max_v < 0 or min_v < 0 else 0
    return int_exp + magni_sep + digit + nega


def magnitude(num, digit=2):
    return f'{num:,.{digit}f}'


def currency(num, digit=2, symbol='$'):
    return f'{symbol}{num:,.{digit}f}'


def accounting(num, digit=2):
    return f'{num:,.{digit}f} ' if num > 0 else f'({abs(num):,.{digit}f})'


def percent(num, digit=2):
    return f'{num:,.{digit}%}'


def magnitudes(numbers, digit=2):
    len_max = max_len(numbers, digit)
    return [f'{magnitude(x, digit): >{len_max}}' for x in numbers]


def currencies(numbers, digit=2, symbol='$'):
    len_max = max_len(numbers, digit) + 1
    return [f'{currency(x, digit, symbol): >{len_max}}' for x in numbers]


def accountings(numbers, digit=2):
    len_max = max_len(numbers, digit) + 1
    return [f'{accounting(x, digit): >{len_max}}' for x in numbers]


def percents(numbers, digit=2):
    len_max = max_len(numbers, digit, is_pct=True) + 1
    return [f'{percent(x, digit): >{len_max}}' for x in numbers]
