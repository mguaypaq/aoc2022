#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 18

>>> part1(TEST_INPUT)
64
>>> part2(TEST_INPUT)
58
"""

import sys

TEST_INPUT = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""


def parse(input):
    return {
        (int(x), int(y), int(z))
        for x, y, z in (
            line.split(',', maxsplit=2)
            for line in input.splitlines()
        )}


def neighbours(cube):
    x, y, z = cube
    return [
        (x+1, y, z),
        (x-1, y, z),
        (x, y+1, z),
        (x, y-1, z),
        (x, y, z+1),
        (x, y, z-1),
    ]


def part1(input):
    cubes = parse(input)
    return sum(
        neighbour not in cubes
        for cube in cubes
        for neighbour in neighbours(cube)
    )


def part2(input):
    cubes = parse(input)

    min_corner = tuple(
        min(c[i] for c in cubes) - 1
        for i in range(3)
    )

    max_corner = tuple(
        max(c[i] for c in cubes) + 1
        for i in range(3)
    )

    area = 0
    steam = set()
    stack = [min_corner]
    while stack:
        cube = stack.pop()
        if all(i <= j <= k for i, j, k in zip(min_corner, cube, max_corner)):
            if cube in cubes:
                area += 1
            elif cube in steam:
                pass
            else:
                steam.add(cube)
                stack.extend(neighbours(cube))
    return area


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
