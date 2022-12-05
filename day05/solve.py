#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 5

>>> part1(TEST_INPUT)
'CMZ'
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import re
import sys

TEST_INPUT = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""  # noqa: W291


def part1(input):
    lines = iter(input.splitlines())

    # first line tells us how many stacks
    line = next(lines)
    if len(line) % 4 != 3:
        raise ValueError(f'invalid drawing line length: {len(line)}')
    num_stacks = (len(line)+1) // 4
    stacks = [[] for _ in range(num_stacks)]

    # read the stack contents from the drawing
    crates_re = re.compile(f'(?:\\[.\\] |    ){{{num_stacks}}}')
    while crates_re.fullmatch(line + ' '):
        for i, stack in enumerate(stacks):
            if line[4*i] == '[':
                stack.append(line[4*i+1])
        line = next(lines)
    for s in stacks:
        s.reverse()

    # assume the next line contains the stack labels
    labels_re = re.compile(f'(?: .  ){{{num_stacks}}}')
    if labels_re.fullmatch(line + ' '):
        stacks = dict(zip(line[1::4], stacks))
    else:
        raise ValueError(f'invalid drawing line: {line!r}')

    # next should be a blank line as separator
    line = next(lines)
    if line:
        raise ValueError(f'extra drawing line: {line!r}')

    # finally, the manipulation instructions
    move_re = re.compile(r'move (0|[1-9]\d*) from (.) to (.)')
    for line in lines:
        m = move_re.fullmatch(line)
        if not m:
            raise ValueError(f'invalid move: {line!r}')
        quantity, source, destination = m.groups()
        if source == destination:
            raise ValueError(f'invalid move: {line!r}')
        for _ in range(int(quantity)):
            crate = stacks[source].pop()
            stacks[destination].append(crate)

    return ''.join(s[-1] for s in stacks.values())


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
