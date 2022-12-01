#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 1

>>> part1(TEST_INPUT)
24000
>>> part2(TEST_INPUT)
45000
>>> list(elves(TEST_INPUT))
[6000, 4000, 11000, 24000, 10000]
"""

import sys

TEST_INPUT = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


def elves(input):
    calories = 0
    for line in input.splitlines():
        if line:
            calories += int(line)
        else:
            yield calories
            calories = 0
    yield calories


def part1(input):
    return max(elves(input))


def part2(input):
    return sum(sorted(elves(input))[-3:])


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
