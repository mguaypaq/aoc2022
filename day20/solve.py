#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 20

>>> part1(TEST_INPUT)
3
>>> part2(TEST_INPUT)
1623178306
"""

import sys

TEST_INPUT = """\
1
2
-3
3
-2
0
4
"""

key = 811589153


def mix(data, pos):
    for i, n in enumerate(data):
        src = pos[i]
        dst = (src + n) % (len(data) - 1)
        for j in range(len(pos)):
            pos[j] -= (pos[j] > src)
            pos[j] += (pos[j] >= dst)
        pos[i] = dst


def grove(data, pos):
    zero = pos[data.index(0)]
    return sum(
        data[pos.index((zero + i) % len(data))]
        for i in [1000, 2000, 3000]
    )


def part1(input):
    data = [int(line) for line in input.splitlines()]
    pos = list(range(len(data)))
    mix(data, pos)
    return grove(data, pos)


def part2(input):
    data = [key * int(line) for line in input.splitlines()]
    pos = list(range(len(data)))
    for _ in range(10):
        mix(data, pos)
    return grove(data, pos)


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
