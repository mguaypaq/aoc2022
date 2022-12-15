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


def part1(input, y):
    sensors, beacons = parse(input)
    boundaries = []
    for sx, sy, sd in sensors:
        radius = sd - abs(sy-y)
        if radius >= 0:
            boundaries.extend([
                (sx-radius,   +1),
                (sx+radius+1, -1),
            ])
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


def scanned(sensors, x, y):
    return any(
        abs(sx-x) + abs(sy-y) <= sd
        for sx, sy, sd in sensors
    )


def part2(input, bound):
    sensors, _ = parse(input)

    # the diagonal lines of the form
    # y = -x + C  and  y = x - C
    # which are 1 or 2 steps outside of each sensor's bubble
    diagonals = set()
    antidiags = set()
    for sx, sy, sd in sensors:
        diagonals.update(
            sx + sy + delta
            for delta in [-sd-2, -sd-1, sd+1, sd+2]
        )
        antidiags.update(
            sx - sy + delta
            for delta in [-sd-2, -sd-1, sd+1, sd+2]
        )

    # the four corners of the region are candidates
    candidates = {(x, y) for x in [0, bound] for y in [0, bound]}
    # the intersections of diagonals and antidiagonals are candidates
    candidates.update(
        ((u+v) // 2, (u-v) // 2)
        for u in diagonals
        for v in antidiags
        if u % 2 == v % 2
    )
    return next(
        4_000_000*x + y
        for (x, y) in candidates
        if 0 <= x <= bound
        and 0 <= y <= bound
        and not scanned(sensors, x, y)
    )


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
