#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 8

>>> part1(TEST_INPUT)
21
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import sys

TEST_INPUT = """\
30373
25512
65332
33549
35390
"""


def part1(input):
    grid = [list(map(int, line)) for line in input.splitlines()]
    nrows = len(grid)
    ncols = len(grid[0])
    if any(len(row) != ncols for row in grid):
        raise ValueError('non-rectangular grid')
    invisible = 0
    for y, row in enumerate(grid):
        for x, tree in enumerate(row):
            col = [r[x] for r in grid]
            invisible += (
                any(t >= tree for t in row[:x])
                and any(t >= tree for t in row[x+1:])
                and any(t >= tree for t in col[:y])
                and any(t >= tree for t in col[y+1:])
            )
    return nrows * ncols - invisible


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
