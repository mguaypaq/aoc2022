#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 22

>>> part1(TEST_INPUT)
6032
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import re
import sys

TEST_INPUT = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

input_re = re.compile(
    r'(?P<board>'
    r'(?:[ .#]+\n)+'
    r')\n'
    r'(?P<path>'
    r'[1-9]\d*(?:[LR][1-9]\d*)*'
    r')\n'
)


def steps(path):
    i = 0
    for j, char in enumerate(path):
        if char in 'LR':
            yield int(path[i:j])
            yield char
            i = j+1
    yield int(path[i:])


def part1(input):
    m = input_re.fullmatch(input)
    if m is None:
        raise ValueError('bad input')
    board = {}
    for row, line in enumerate(m['board'].splitlines(), 1):
        for col, char in enumerate(line, 1):
            if char in '.#':
                board[row, col] = char
    r, c = min(board.keys())
    facing = '>'
    delta = {
        '>': (0, +1),
        'v': (+1, 0),
        '<': (0, -1),
        '^': (-1, 0),
    }
    turn_left = dict(zip('>v<^', '^>v<'))
    turn_right = dict(zip('>v<^', 'v<^>'))
    for step in steps(m['path']):
        if step == 'L':
            facing = turn_left[facing]
        elif step == 'R':
            facing = turn_right[facing]
        else:
            for _ in range(step):
                dr, dc = delta[facing]
                new_r, new_c = r+dr, c+dc
                if (new_r, new_c) not in board:
                    while (new_r-dr, new_c-dc) in board:
                        new_r, new_c = new_r-dr, new_c-dc
                if board[new_r, new_c] == '#':
                    break
                r, c = new_r, new_c
    return 1000*r + 4*c + '>v<^'.index(facing)


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
