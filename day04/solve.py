#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 4

>>> part1(TEST_INPUT)
2
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import re
import sys

TEST_INPUT = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

line_re = re.compile(r"""
    (0|[1-9][0-9]*)    # 1st number
    -(0|[1-9][0-9]*),  # 2nd number
    (0|[1-9][0-9]*)    # 3rd number
    -(0|[1-9][0-9]*)   # 4th number
""", re.VERBOSE)


def part1(input):
    contained = 0
    for line in input.splitlines():
        m = line_re.fullmatch(line)
        if m is None:
            raise ValueError(f'invalid line: {line!r}')
        a, b, c, d = map(int, m.groups())
        if b < a or d < c:
            raise ValueError(f'invalid ranges: {line!r}')
        contained += (a <= c <= d <= b) or (c <= a <= b <= d)
    return contained


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
