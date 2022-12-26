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


def int_from_snafu(line):
    n = 0
    for char in line:
        n = n*5 + '=-012'.index(char) - 2
    return n


def snafu_from_int(n):
    chars = []
    while n:
        n, d = divmod(n+2, 5)
        chars.append('=-012'[d])
    return ''.join(reversed(chars))


def part1(input):
    return snafu_from_int(sum(
        int_from_snafu(line) for line in input.splitlines()
    ))


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
