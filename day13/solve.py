#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 13

>>> part1(TEST_INPUT)
13
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import sys

TEST_INPUT = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""


# Matched parentheses is famously a context-free language
# rather than a regular language, so regexp won't suffice!
def parse(line):
    stack = []
    i = 0
    while i < len(line):
        if line[i:i+2] == '[]':
            item = []
            i += 2
        elif line[i] == '[':
            stack.append([])
            i += 1
            continue
        elif line[i].isdigit():
            j = i + 1
            while j < len(line) and line[j].isdigit():
                j += 1
            item = int(line[i:j])
            i = j
        else:
            raise ValueError
        while i < len(line) and line[i] == ']':
            stack[-1].append(item)
            item = stack.pop()
            i += 1
        if i < len(line) and line[i] == ',':
            stack[-1].append(item)
            i += 1
        elif i == len(line):
            break
        else:
            raise ValueError
    else:
        raise ValueError
    if stack:
        raise ValueError
    if isinstance(item, int):
        raise ValueError
    return item


def compare(left, right):
    if isinstance(left, int):
        if isinstance(right, int):
            return (left > right) - (left < right)
        else:
            return compare([left], right)
    else:
        if isinstance(right, int):
            return compare(left, [right])
        else:
            for left_item, right_item in zip(left, right):
                c = compare(left_item, right_item)
                if c != 0:
                    return c
            return compare(len(left), len(right))


def part1(input):
    lines = iter(input.splitlines())
    pairs = []
    while True:
        pairs.append((parse(next(lines)), parse(next(lines))))
        try:
            blank = next(lines)
        except StopIteration:
            break
        if blank:
            raise ValueError
    if any(
        compare(left, right) == 0
        for left, right in pairs
    ):
        raise ValueError
    return sum(
        index
        for index, (left, right) in enumerate(pairs, 1)
        if compare(left, right) < 0
    )


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
