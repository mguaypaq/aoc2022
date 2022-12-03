#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 3

>>> part1(TEST_INPUT)
157
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import string
import sys

TEST_INPUT = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


def part1(input):
    priority = {letter: p for p, letter in enumerate(string.ascii_letters, 1)}
    total = 0
    for rucksack in input.splitlines():
        size = len(rucksack)
        if size % 2 != 0:
            raise ValueError(f'unequal compartment sizes: {rucksack!r}')
        overlap = set(rucksack[:size//2]) & set(rucksack[size//2:])
        if len(overlap) != 1:
            raise ValueError(f'non-unique overlap: {rucksack!r}')
        total += priority[overlap.pop()]
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
