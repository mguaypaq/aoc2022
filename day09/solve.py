#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 9

>>> part1(TEST_INPUT)
13
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import re
import sys

TEST_INPUT = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

move_re = re.compile(r'([UDLR]) (0|[1-9]\d*)')

step = {
    'U': lambda p: (p[0], p[1]+1),
    'D': lambda p: (p[0], p[1]-1),
    'L': lambda p: (p[0]-1, p[1]),
    'R': lambda p: (p[0]+1, p[1]),
}


def distance(p, q):
    return max(abs(i-j) for i, j in zip(p, q))


def part1(input):
    head = tail = (0, 0)
    visited = {tail}
    for line in input.splitlines():
        m = move_re.fullmatch(line)
        if m is None:
            raise ValueError(f'invalid move: {line!r}')
        direction, count = m.groups()
        for _ in range(int(count)):
            new = step[direction](head)
            if distance(new, tail) > 1:
                tail = head
                visited.add(tail)
            head = new
    return len(visited)


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
