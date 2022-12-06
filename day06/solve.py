#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 6

>>> [part1(input) for input in TEST_INPUT]
[7, 5, 6, 10, 11]
>>> [part2(input) for input in TEST_INPUT]
[19, 23, 23, 29, 26]
"""

import sys

TEST_INPUT = [
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
]


def marker(input, size):
    return next(
        i for i in range(size, len(input))
        if len(set(input[i-size:i])) == size
    )


def part1(input):
    return marker(input, 4)


def part2(input):
    return marker(input, 14)


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
