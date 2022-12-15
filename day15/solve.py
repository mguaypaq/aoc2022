#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 15

>>> part1(TEST_INPUT, y=10)
26
>>> part2(TEST_INPUT, bound=20)
56000011
"""

import re
import sys

TEST_INPUT = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

num = r'(0|-?[1-9]\d*)'
line_re = re.compile(
    f'Sensor at x={num}, y={num}: closest beacon is at x={num}, y={num}'
)


def parse(input):
    sensors = []
    beacons = set()
    for line in input.splitlines():
        m = line_re.fullmatch(line)
        if m is None:
            raise ValueError(f'bad line: {line!r}')
        sx, sy, bx, by = map(int, m.groups())
        sd = abs(sx-bx) + abs(sy-by)
        sensors.append((sx, sy, sd))
        beacons.add((bx, by))
    return sensors, beacons


def intersect(sensors, y):
    boundaries = []
    for sx, sy, sd in sensors:
        radius = sd - abs(sy-y)
        if radius >= 0:
            boundaries.extend([
                (sx - radius,     +1),
                (sx + radius + 1, -1),
            ])
    return boundaries


def part1(input, y):
    sensors, beacons = parse(input)

    boundaries = intersect(sensors, y)
    boundaries.sort()
    signal = 0
    excluded = 0
    for x, s in boundaries:
        if not signal:
            excluded -= x
        signal += s
        assert signal >= 0
        if not signal:
            excluded += x

    return excluded - sum((by == y) for (bx, by) in beacons)


def part2(input, bound):
    sensors, beacons = parse(input)

    for y in range(bound+1):
        boundaries = intersect(sensors, y)
        boundaries.extend([
            (0,       -1),
            (bound+1, +1),
        ])
        boundaries.sort(key=lambda x: (x[0], -x[1]))
        signal = 1
        for x, s in boundaries:
            signal += s
            if not signal:
                return 4_000_000*x + y
    raise ValueError('not found')


def main(args):
    input = open('input.txt').read()
    if args == ['1']:
        print(part1(input, y=2_000_000), file=open('output1.txt', 'w'))
    elif args == ['2']:
        print(part2(input, bound=4_000_000), file=open('output2.txt', 'w'))
    else:
        raise ValueError(f'invalid arguments: {args!r}')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
