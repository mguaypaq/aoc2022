#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 8

>>> part1(TEST_INPUT)
21
>>> part2(TEST_INPUT)
8
"""

import sys

TEST_INPUT = """\
30373
25512
65332
33549
35390
"""


def parse(input):
    rows = tuple(
        tuple(int(tree) for tree in row)
        for row in input.splitlines()
    )
    cols = tuple(zip(*rows, strict=True))
    return rows, cols


def part1(input):
    rows, cols = parse(input)
    visible = len(rows) * len(cols)
    for x, col in enumerate(cols):
        for y, row in enumerate(rows):
            tree = row[x]
            assert tree == col[y]
            visible -= (
                any(t >= tree for t in row[:x])
                and any(t >= tree for t in row[x+1:])
                and any(t >= tree for t in col[:y])
                and any(t >= tree for t in col[y+1:])
            )
    return visible


def view(ray):
    tree, *ray = ray
    result = 0
    for t in ray:
        result += 1
        if t >= tree:
            break
    return result


def part2(input):
    rows, cols = parse(input)
    return max(
        view(row[x:]) * view(row[x::-1]) * view(col[y:]) * view(col[y::-1])
        for x, col in enumerate(cols)
        for y, row in enumerate(rows)
    )


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
