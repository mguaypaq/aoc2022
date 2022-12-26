#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 25

>>> part1(TEST_INPUT)
'2=-1=0'
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import sys

TEST_INPUT = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""


def part1(input):
    digits = []
    for line in input.splitlines():
        place = 0
        carry = 0
        while place < len(line) or carry:
            while place >= len(digits):
                digits.append(0)
            digit = digits[place]
            if place < len(line):
                digit += '=-012'.index(line[-1-place]) - 2
            digit += carry
            if digit < -2:
                digit += 5
                carry = -1
            elif digit > 2:
                digit -= 5
                carry = 1
            else:
                carry = 0
            assert -2 <= digit <= 2
            digits[place] = digit
            place += 1
    while digits and digits[-1] == 0:
        digits.pop()
    return ''.join('012=-'[d] for d in reversed(digits))


def part2(input):
    raise NotImplementedError


def main(args):
    input = open('input.txt').read()
    if args == ['1']:
        print(part1(input), file=open('output1.txt', 'w'))
    elif args == ['2']:
        print(part2(input), file=open('output2.txt', 'w'))
    else:
        raise ValueError(f'invalid arguments: {args!r}')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
