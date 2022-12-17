#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 17

>>> part1(TEST_INPUT)
3068
>>> part2(TEST_INPUT)
1514285714288
"""

import re
import sys
from typing import NamedTuple

TEST_INPUT = """\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""

input_re = re.compile(r'(?P<jets>[<>]+)\n')


class Shape(NamedTuple):
    width: int
    height: int
    # blocks[0] is the top block of the leftmost column
    blocks: list[tuple[int, int]]


shapes = [
    Shape(4, 1, [(0, 0), (1, 0), (2, 0), (3, 0)]),
    Shape(3, 3, [(0, 1), (1, 2), (1, 1), (1, 0), (2, 1)]),
    Shape(3, 3, [(0, 0), (1, 0), (2, 2), (2, 1), (2, 0)]),
    Shape(1, 4, [(0, 3), (0, 2), (0, 1), (0, 0)]),
    Shape(2, 2, [(0, 1), (0, 0), (1, 1), (1, 0)]),
]


class Simulation:
    def __init__(self, jets):
        self.shape_index = 0
        self.jets = jets
        self.jet_index = 0
        self.blocks = {(x, 0) for x in range(7)}
        self.left_y = 0
        self.top_y = 0
        self.scrolled = 0

    def __str__(self):
        lines = ['+-------+']
        for y in range(1, self.top_y + 1):
            line = ''.join(
                '#' if (x, y) in self.blocks else '.'
                for x in range(7)
            )
            lines.append(f'|{line}|')
        return '\n'.join(reversed(lines))

    def height(self):
        return self.top_y + self.scrolled

    def get_shape(self):
        shape = shapes[self.shape_index]
        self.shape_index += 1
        if self.shape_index == len(shapes):
            self.shape_index = 0
        return shape

    def get_jet(self):
        jet = self.jets[self.jet_index]
        self.jet_index += 1
        if self.jet_index == len(self.jets):
            self.jet_index = 0
        return jet

    def drop_rock(self):
        rx, ry = 2, self.top_y + 4
        width, height, blocks = self.get_shape()

        while True:
            jet = self.get_jet()
            rx += jet
            if (rx < 0
                or 7 < rx+width
                or any(
                    (rx+bx, ry+by) in self.blocks
                    for bx, by in blocks
                    )):
                rx -= jet

            ry -= 1
            if any(
                (rx+bx, ry+by) in self.blocks
                for bx, by in blocks
            ):
                ry += 1
                break

        self.blocks.update(
            (rx+bx, ry+by)
            for bx, by in blocks
        )
        if rx == 0:
            bx, by = blocks[0]
            self.left_y = max(self.left_y, ry+by)
        self.top_y = max(self.top_y, ry+height-1)

    def scroll(self):
        x, y = 0, self.left_y
        assert (x, y) in self.blocks
        assert (x, y+1) not in self.blocks
        outline = {(x, y)}
        direction = 'R'
        moves = {
            'R': [(+1, +1, 'U'), (+1, 0, 'R'), (0, 0, 'D')],
            'U': [(-1, +1, 'L'), (0, +1, 'U'), (0, 0, 'R')],
            'L': [(-1, -1, 'D'), (-1, 0, 'L'), (0, 0, 'U')],
            'D': [(+1, -1, 'R'), (0, -1, 'D'), (0, 0, 'L')],
        }
        while x != 6:
            for dx, dy, direction in moves[direction]:
                if (x+dx, y+dy) in self.blocks:
                    x += dx
                    y += dy
                    break
            outline.add((x, y))
        scrolled = min(y for (x, y) in outline)
        self.blocks = {(x, y-scrolled) for (x, y) in outline}
        self.left_y -= scrolled
        self.top_y -= scrolled
        self.scrolled += scrolled

    def equivalent(self, other):
        if (self.shape_index == other.shape_index
                and self.jet_index == other.jet_index):
            self.scroll()
            other.scroll()
            return self.blocks == other.blocks
        return False


def parse(input):
    m = input_re.fullmatch(input)
    if m is None:
        raise ValueError('bad input')
    return [
        -1 if char == '<' else +1
        for char in m['jets']
    ]


def part1(input):
    simulation = Simulation(parse(input))
    for _ in range(2022):
        simulation.drop_rock()
    return simulation.height()


def part2(input):
    jets = parse(input)
    slow = Simulation(jets)
    fast = Simulation(jets)
    fallen = 0
    cycle = None
    while fallen < 1_000_000_000_000:
        slow.drop_rock()
        fallen += 1
        if cycle is None:
            fast.drop_rock()
            fast.drop_rock()
            if slow.equivalent(fast):
                cycle = fallen
                repeats = (1_000_000_000_000 - fallen) // cycle
                slow.scrolled += repeats * (fast.height() - slow.height())
                fallen += repeats * cycle
    return slow.height()


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
