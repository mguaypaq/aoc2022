#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 2

>>> part1(TEST_INPUT)
15
>>> part2(TEST_INPUT)
12
"""

import re
import sys

TEST_INPUT = """\
A Y
B X
C Z
"""

LINE_RE = re.compile(r'([ABC]) ([XYZ])')


def score(input, scoring):
    total = 0
    for line in input.splitlines():
        m = LINE_RE.fullmatch(line)
        if m is None:
            raise ValueError(f'invalid line: {line!r}')
        total += scoring[m.groups()]
    return total


def part1(input):
    return score(input, {
        ('A', 'X'): 1 + 3,
        ('A', 'Y'): 2 + 6,
        ('A', 'Z'): 3 + 0,
        ('B', 'X'): 1 + 0,
        ('B', 'Y'): 2 + 3,
        ('B', 'Z'): 3 + 6,
        ('C', 'X'): 1 + 6,
        ('C', 'Y'): 2 + 0,
        ('C', 'Z'): 3 + 3,
    })


def part2(input):
    return score(input, {
        ('A', 'X'): 3 + 0,
        ('A', 'Y'): 1 + 3,
        ('A', 'Z'): 2 + 6,
        ('B', 'X'): 1 + 0,
        ('B', 'Y'): 2 + 3,
        ('B', 'Z'): 3 + 6,
        ('C', 'X'): 2 + 0,
        ('C', 'Y'): 3 + 3,
        ('C', 'Z'): 1 + 6,
    })


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
