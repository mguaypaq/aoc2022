#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 20

>>> part1(TEST_INPUT)
3
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
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


def part1(input):
    data = [(int(line), False) for line in input.splitlines()]
    i = 0
    while i < len(data):
        if data[i][1]:
            i += 1
        else:
            n, _ = data.pop(i)
            j = (i + n) % len(data)
            data.insert(j, (n, True))
    data = [n for n, _ in data]
    z = data.index(0)
    return sum(data[(z+i) % len(data)] for i in [1000, 2000, 3000])


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
