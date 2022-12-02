#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 2

>>> part1(TEST_INPUT)
15
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import re
import sys

TEST_INPUT = """\
A Y
B X
C Z
"""

LINE_RE = re.compile(r'([ABC]) ([XYZ])')


def part1(input):
    scoring = {
        ('A', 'X'): 1 + 3,
        ('A', 'Y'): 2 + 6,
        ('A', 'Z'): 3 + 0,
        ('B', 'X'): 1 + 0,
        ('B', 'Y'): 2 + 3,
        ('B', 'Z'): 3 + 6,
        ('C', 'X'): 1 + 6,
        ('C', 'Y'): 2 + 0,
        ('C', 'Z'): 3 + 3,
    }

    total = 0
    for line in input.splitlines():
        m = LINE_RE.fullmatch(line)
        if m is None:
            raise ValueError(f'invalid line: {line!r}')
        total += scoring[m.groups()]
    return total


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
