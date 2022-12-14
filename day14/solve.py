#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 14

>>> part1(TEST_INPUT)
24
>>> part2(TEST_INPUT)
93
"""

import re
import sys

TEST_INPUT = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

int_re = r'(?:0|[1-9]\d*)'
point_re = f'{int_re},{int_re}'
line_re = re.compile(f'{point_re}(?: -> {point_re})*')


def parse(input):
    for line in input.splitlines():
        if not line_re.fullmatch(line):
            raise ValueError(f'invalid line: {line!r}')
        yield [
            tuple(int(coord) for coord in point.split(','))
            for point in line.split(' -> ')
        ]


def path(points):
    points = iter(points)
    src = next(points)
    for dst in points:
        if sum((s != d) for s, d in zip(src, dst)) != 1:
            raise ValueError(f'diagonal segment from {src} to {dst}')
        while src != dst:
            yield src
            src = tuple(s + (d > s) - (d < s) for s, d in zip(src, dst))
    yield src


def part1(input):
    blocks = set()
    for points in parse(input):
        blocks.update(path(points))
    abyss = max(y for (x, y) in blocks)

    resting = 0
    while True:
        x, y = sand = (500, 0)
        if sand in blocks:
            raise ValueError('blocked source')
        while y < abyss:
            for down in [(x, y+1), (x-1, y+1), (x+1, y+1)]:
                if down not in blocks:
                    x, y = sand = down
                    break
            else:
                break
        else:
            break
        blocks.add(sand)
        resting += 1
    return resting


def part2(input):
    blocks = set()
    for points in parse(input):
        blocks.update(path(points))
    floor = max(y+1 for (x, y) in blocks)

    resting = 0
    while True:
        x, y = sand = (500, 0)
        if sand in blocks:
            break
        while y < floor:
            for down in [(x, y+1), (x-1, y+1), (x+1, y+1)]:
                if down not in blocks:
                    x, y = sand = down
                    break
            else:
                break
        blocks.add(sand)
        resting += 1
    return resting


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
