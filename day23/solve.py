#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 23

>>> part1(TEST_INPUT)
110
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import collections
import sys
from typing import NamedTuple

TEST_INPUT = """\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""


class Point(NamedTuple):
    row: int
    col: int

    def __add__(self, other):
        return Point(*(a + b for a, b in zip(self, other)))


def part1(input):
    elves = set()
    for row, line in enumerate(input.splitlines()):
        for col, char in enumerate(line):
            if char == '.':
                pass
            elif char == '#':
                elves.add(Point(row, col))
            else:
                raise ValueError(f'bad character: {char!r}')
    conditions = [
        (Point(0, 0), [
            Point(-1, -1), Point(-1, 0), Point(-1, +1), Point(0, -1),
            Point(0, +1), Point(+1, -1), Point(+1, 0), Point(+1, +1),
        ]),
        (Point(-1, 0), [
            Point(-1, -1), Point(-1, 0), Point(-1, +1),
        ]),
        (Point(+1, 0), [
            Point(+1, -1), Point(+1, 0), Point(+1, +1),
        ]),
        (Point(0, -1), [
            Point(-1, -1), Point(0, -1), Point(+1, -1),
        ]),
        (Point(0, +1), [
            Point(-1, +1), Point(0, +1), Point(+1, +1),
        ]),
        (Point(0, 0), []),
    ]
    for _ in range(10):
        proposal = {}
        for elf in elves:
            proposal[elf] = elf + next(
                direction
                for direction, blockers in conditions
                if all(
                    elf + blocker not in elves
                    for blocker in blockers
                )
            )
        count = collections.Counter(proposal.values())
        next_elves = {
            destination if count[destination] == 1 else source
            for source, destination in proposal.items()
        }
        assert len(next_elves) == len(elves)
        elves = next_elves
        conditions[1:5] = conditions[2:5] + conditions[1:2]
    min_row = min(r for r, c in elves)
    min_col = min(c for r, c in elves)
    max_row = max(r for r, c in elves)
    max_col = max(c for r, c in elves)
    return (max_row - min_row + 1) * (max_col - min_col + 1) - len(elves)


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
