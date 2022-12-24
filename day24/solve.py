#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 24

>>> part1(TEST_INPUT)
18
>>> part2(TEST_INPUT)
54
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


def parse(input):
    lines = input.splitlines()
    if len(lines) < 3:
        raise ValueError('not enough lines')
    if any(len(line) != len(lines[0]) for line in lines):
        raise ValueError('uneven lines')

    top, *mid, bot = lines
    m = cliff_re.fullmatch(top)
    if m is None:
        raise ValueError('invalid top line')
    start = (m.start('hole')-1, 0)
    m = cliff_re.fullmatch(bot)
    if m is None:
        raise ValueError('invalid bottom line')
    goal = (m.start('hole')-1, len(mid)-1)

    board = []
    for line in mid:
        m = valley_re.fullmatch(line)
        if m is None:
            raise ValueError('invalid middle line')
        board.append(m['hole'])

    return start, goal, board


def walk(time, start, goal, board):
    height = len(board)
    width = len(board[0])
    current = set()
    while goal not in current:
        time += 1
        current = {
            (x+dx, y+dy)
            for x, y in current
            for dx, dy in [(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)]
        }
        current.add(start)
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


def part1(input):
    start, goal, board = parse(input)
    return walk(0, start, goal, board)


def part2(input):
    start, goal, board = parse(input)
    time = walk(0, start, goal, board)
    time = walk(time, goal, start, board)
    return walk(time, start, goal, board)


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
