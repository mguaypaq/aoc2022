#!/usr/bin/python3
"""
Advent of Code 2022 -- Day {{day}}

>>> part1(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import sys

TEST_INPUT = """\
"""


def part1(input):
    raise NotImplementedError


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
