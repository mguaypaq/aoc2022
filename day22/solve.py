#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 22

>>> part1(TEST_INPUT, tile_size=4)
6032
>>> part2(TEST_INPUT, tile_size=4)
5031
"""

import itertools as it
import sys
from typing import NamedTuple

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


class Vector(NamedTuple):
    row: int
    col: int

    def __add__(self, other):
        return Vector(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other):
        return Vector(*(a - b for a, b in zip(self, other)))

    def __mod__(self, other):
        return Vector(*(a % b for a, b in zip(self, other)))

    def __le__(self, other):
        return all(a <= b for a, b in zip(self, other))

    def __lt__(self, other):
        return all(a < b for a, b in zip(self, other))

    def rotate(self, count, tile_size=1):
        row, col = self
        for _ in range(count % 4):
            row, col = col, (tile_size - 1 - row)
        return Vector(row, col)


zero = Vector(0, 0)

facings = [
    Vector(0, +1),
    Vector(+1, 0),
    Vector(0, -1),
    Vector(-1, 0),
]

facing_char = dict(zip(facings, '>v<^'))


class Tile:
    offset: Vector
    chars: list[list[str]]
    neighbours: dict[Vector, tuple['Tile', int]]

    def __init__(self, offset, chars):
        self.offset = offset
        self.chars = chars
        self.neighbours = {}

    def __bool__(self):
        return self.chars[0][0] != ' '

    def size(self):
        return len(self.chars)


class Position(NamedTuple):
    tile: Tile
    offset: Vector
    facing: Vector

    def turn(self, count):
        tile, offset, facing = self
        return Position(tile, offset, facing.rotate(count))

    def step(self):
        tile, offset, facing = self
        size = Vector(tile.size(), tile.size())
        offset += facing
        if zero <= offset < size:
            pass  # stay in the same tile
        else:
            tile, turn = tile.neighbours[facing]
            offset = offset % size
            offset = offset.rotate(turn, tile.size())
            facing = facing.rotate(turn)
        return Position(tile, offset, facing)

    def is_wall(self):
        row, col = self.offset
        return self.tile.chars[row][col] == '#'

    def mark(self):
        row, col = self.offset
        self.tile.chars[row][col] = facing_char[self.facing]

    def password(self):
        row, col = self.tile.offset + self.offset
        return 1000*row + 4*col + facings.index(self.facing)


class Board:
    tiles: list[list[Tile]]
    path: str

    def __init__(self, input, tile_size):
        lines = input.splitlines()

        if len(lines) < 2:
            raise ValueError('not enough input lines')
        self.path = lines.pop()
        if lines.pop() != "":
            raise ValueError('missing blank line')

        if len(lines) == 0 or len(lines) % tile_size != 0:
            raise ValueError('missing or incomplete tile columns')
        for outer_row in range(0, len(lines), tile_size):
            length = len(lines[outer_row])
            if length == 0 or length % tile_size != 0:
                raise ValueError('missing or incomplete tile rows')
            for row in range(outer_row, outer_row + tile_size):
                if len(lines[row]) != length:
                    raise ValueError('uneven tile rows')

        tiles = []
        for outer_row in range(0, len(lines), tile_size):
            tile_row = []
            for outer_col in range(0, len(lines[outer_row]), tile_size):
                offset = Vector(outer_row+1, outer_col+1)
                chars = [[
                    lines[row][col]
                    for col in range(outer_col, outer_col + tile_size)]
                    for row in range(outer_row, outer_row + tile_size)]
                if all(char in '.#' for row in chars for char in row):
                    pass  # normal tile
                elif all(char == ' ' for row in chars for char in row):
                    pass  # blank tile
                else:
                    raise ValueError('unexpected character')
                tile = Tile(offset, chars)
                tile_row.append(tile)
            tiles.append(tile_row)
        self.tiles = tiles

    def wrap_flat(self):
        for tile_row in self.tiles:
            tiles = [t for t in tile_row if t]
            if tiles:
                for west, east in zip(tiles, tiles[1:] + tiles[:1]):
                    west.neighbours[Vector(0, +1)] = (east, 0)
                    east.neighbours[Vector(0, -1)] = (west, 0)
        for tile_col in it.zip_longest(*self.tiles):
            tiles = [t for t in tile_col if t]
            if tiles:
                for north, south in zip(tiles, tiles[1:] + tiles[:1]):
                    north.neighbours[Vector(+1, 0)] = (south, 0)
                    south.neighbours[Vector(-1, 0)] = (north, 0)

    def wrap_cube(self):
        tiles = {
            Vector(row, col): tile
            for row, tile_row in enumerate(self.tiles)
            for col, tile in enumerate(tile_row)
            if tile
        }
        faces = {
            'U': dict(zip(facings, [('R', 0), ('F', 0), ('L', 0), ('B', 0)])),
            'F': dict(zip(facings, [('R', 3), ('D', 0), ('L', 1), ('U', 0)])),
            'D': dict(zip(facings, [('R', 2), ('B', 0), ('L', 2), ('F', 0)])),
            'B': dict(zip(facings, [('R', 1), ('U', 0), ('L', 3), ('D', 0)])),
            'L': dict(zip(facings, [('U', 0), ('F', 3), ('D', 2), ('B', 1)])),
            'R': dict(zip(facings, [('D', 2), ('F', 1), ('U', 0), ('B', 3)])),
        }
        face_to_tile = {}
        stack = [(next(iter(tiles.keys())), 'U', 0)]
        while stack:
            pos, face, turn = stack.pop()
            if pos in tiles:
                tile = tiles.pop(pos)
                if face in face_to_tile:
                    raise ValueError('two tiles on the same face')
                face_to_tile[face] = (tile, turn)
                for dpos in facings:
                    newface, dturn = faces[face][dpos.rotate(-turn)]
                    stack.append((pos + dpos, newface, turn - dturn))
        if tiles:
            raise ValueError('disconnected tiles')
        for face, neighbours in faces.items():
            tile, turn = face_to_tile[face]
            for edge, (newface, dturn) in neighbours.items():
                newtile, newturn = face_to_tile[newface]
                tile.neighbours[edge.rotate(turn)] = (
                    newtile,
                    newturn + dturn - turn,
                )

    def initial_position(self):
        tile = next(t for t in self.tiles[0] if t)
        col = next(
            col
            for col, char in enumerate(tile.chars[0])
            if char != '#'
        )
        return Position(tile, Vector(0, col), facings[0])

    def walk(self):
        position = self.initial_position()
        position.mark()
        for step in steps(self.path):
            if step == 'L':
                position = position.turn(-1)
                position.mark()
            elif step == 'R':
                position = position.turn(+1)
                position.mark()
            else:
                for _ in range(step):
                    in_front = position.step()
                    if in_front.is_wall():
                        break
                    else:
                        position = in_front
                        position.mark()
        return position

    def __str__(self):
        return '\n'.join(
            '\n'.join(
                ''.join(
                    ''.join(inner_row)
                    for inner_row in outer_row
                )
                for outer_row in zip(*(tile.chars for tile in tile_row))
            )
            for tile_row in self.tiles
        )


def steps(path):
    i = 0
    for j, char in enumerate(path):
        if char.isdigit():
            pass
        elif char in 'LR':
            yield int(path[i:j])
            yield char
            i = j+1
        else:
            raise ValueError('invalid character')
    yield int(path[i:])


def part1(input, tile_size):
    board = Board(input, tile_size)
    board.wrap_flat()
    pos = board.walk()
    # print(board)
    return pos.password()


def part2(input, tile_size):
    board = Board(input, tile_size)
    board.wrap_cube()
    pos = board.walk()
    # print(board)
    return pos.password()


def main(args):
    input = open('input.txt').read()
    if args == ['1']:
        print(part1(input, tile_size=50), file=open('output1.txt', 'w'))
    elif args == ['2']:
        print(part2(input, tile_size=50), file=open('output2.txt', 'w'))
    else:
        raise ValueError(f'invalid arguments: {args!r}')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
