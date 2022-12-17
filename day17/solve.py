#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 17

>>> part1(TEST_INPUT)
3068
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import itertools as it
import re
import sys

TEST_INPUT = """\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""

input_re = re.compile(r'(?P<jets>[<>]+)\n')


def part1(input):
    m = input_re.fullmatch(input)
    if m is None:
        raise ValueError('bad input')
    jets = it.cycle(m['jets'])

    shapes = it.cycle([
        {(2, 3), (3, 3), (4, 3), (5, 3)},
        {(3, 3), (2, 4), (3, 4), (4, 4), (3, 5)},
        {(2, 3), (3, 3), (4, 3), (4, 4), (4, 5)},
        {(2, 3), (2, 4), (2, 5), (2, 6)},
        {(2, 3), (3, 3), (2, 4), (3, 4)},
    ])

    blocks = set()
    height = 0
    rock = next(shapes)
    fallen = 0
    while fallen < 2022:
        jet = -1 if next(jets) == '<' else +1
        pushed = {(x+jet, y) for (x, y) in rock}
        if all(x in range(7) and (x, y) not in blocks for (x, y) in pushed):
            rock = pushed
        pushed = {(x, y-1) for (x, y) in rock}
        if all(0 <= y and (x, y) not in blocks for (x, y) in pushed):
            rock = pushed
        else:
            blocks.update(rock)
            height = max(y for (x, y) in blocks) + 1
            rock = {(x, y+height) for (x, y) in next(shapes)}
            fallen += 1
    return height


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
