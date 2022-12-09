#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 9

>>> part1(TEST_INPUT_1)
13
>>> part2(TEST_INPUT_1)
1
>>> part2(TEST_INPUT_2)
36
"""

import itertools as it
import re
import sys

TEST_INPUT_1 = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

TEST_INPUT_2 = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""


move_re = re.compile(r'([UDLR]) (0|[1-9]\d*)')

step = {
    'U': lambda p: (p[0], p[1]+1),
    'D': lambda p: (p[0], p[1]-1),
    'L': lambda p: (p[0]-1, p[1]),
    'R': lambda p: (p[0]+1, p[1]),
}


def distance(head, tail):
    return max(abs(h-t) for h, t in zip(head, tail))


def newtail(head, tail):
    if distance(head, tail) > 1:
        tail = tuple(t + (h > t) - (h < t) for h, t in zip(head, tail))
    return tail


def parse(input):
    for line in input.splitlines():
        m = move_re.fullmatch(line)
        if m is None:
            raise ValueError(f'invalid move: {line!r}')
        direction, count = m.groups()
        yield from it.repeat(direction, int(count))


def part1(input):
    head = tail = (0, 0)
    visited = {tail}
    for direction in parse(input):
        head = step[direction](head)
        tail = newtail(head, tail)
        visited.add(tail)
    return len(visited)


def part2(input):
    knots = [(0, 0)] * 10
    visited = {knots[-1]}
    for direction in parse(input):
        knots[0] = step[direction](knots[0])
        for i in range(1, len(knots)):
            knots[i] = newtail(knots[i-1], knots[i])
        visited.add(knots[-1])
    return len(visited)


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
