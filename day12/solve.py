#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 12

>>> part1(TEST_INPUT)
31
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import string
import sys

TEST_INPUT = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

HEIGHT = {c: i for i, c in enumerate(string.ascii_lowercase)}
HEIGHT['S'] = HEIGHT['a']
HEIGHT['E'] = HEIGHT['z']


def part1(input):
    height = {}
    start = stop = None
    for x, line in enumerate(input.splitlines()):
        for y, char in enumerate(line):
            height[x, y] = HEIGHT[char]
            if char == 'S':
                start = (x, y)
            elif char == 'E':
                stop = (x, y)
    if start is None:
        raise ValueError('missing start')
    if stop is None:
        raise ValueError('missing stop')

    step = 0
    visited = set()
    curpos = {start}
    while curpos:
        if stop in curpos:
            break
        step += 1
        newpos = set()
        for x, y in curpos - visited:
            for neighbour in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if height.get(neighbour, float('inf')) <= height[x, y] + 1:
                    newpos.add(neighbour)
        visited |= curpos
        curpos = newpos
    else:
        raise ValueError('goal unreachable')
    return step


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
