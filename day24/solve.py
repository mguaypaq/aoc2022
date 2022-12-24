#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 24

>>> part1(TEST_INPUT)
18
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import re
import sys

TEST_INPUT = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""

cliff_re = re.compile(r'#+(?P<hole>\.)#+')
valley_re = re.compile(r'#(?P<hole>[>v<^.]+)#')


def part1(input):
    lines = input.splitlines()
    if len(lines) < 3:
        raise ValueError('not enough lines')
    if any(len(line) != len(lines[0]) for line in lines):
        raise ValueError('uneven lines')

    height = len(lines) - 2
    width = len(lines[0]) - 2

    top, *mid, bot = lines
    m = cliff_re.fullmatch(top)
    if m is None:
        raise ValueError('invalid top line')
    start = (m.start('hole')-1, -1)
    m = cliff_re.fullmatch(bot)
    if m is None:
        raise ValueError('invalid bottom line')
    goal = (m.start('hole')-1, height-1)

    board = []
    for line in mid:
        m = valley_re.fullmatch(line)
        if m is None:
            raise ValueError('invalid middle line')
        board.append(m['hole'])

    time = 0
    current = set()
    while goal not in current:
        time += 1
        current.add(start)
        current = {
            (x+dx, y+dy)
            for x, y in current
            for dx, dy in [(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)]
        }
        current = {
            (x, y)
            for x, y in current
            if 0 <= x < width
            and 0 <= y < height
            and board[y][(x-time) % width] != '>'
            and board[(y-time) % height][x] != 'v'
            and board[y][(x+time) % width] != '<'
            and board[(y+time) % height][x] != '^'
        }
    return time + 1


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
