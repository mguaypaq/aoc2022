#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 21

>>> part1(TEST_INPUT)
152
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import re
import sys

TEST_INPUT = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""

line_re = re.compile(
    r'(?P<monkey>[a-z]{4}): '
    r'(?:(?P<number>0|-?[1-9]\d*)'
    r'|(?P<left>[a-z]{4}) (?P<op>[+\-*/]) (?P<right>[a-z]{4}))'
)


def part1(input):
    value = {}
    expr = {}
    for line in input.splitlines():
        m = line_re.fullmatch(line)
        if m is None:
            raise ValueError(f'bad line: {line!r}')
        if m['number'] is not None:
            value[m['monkey']] = int(m['number'])
        else:
            expr[m['monkey']] = (m['left'], m['op'], m['right'])

    stack = [('root', False)]
    active = set()
    while stack:
        monkey, ready = stack.pop()
        if not ready:
            if monkey not in value:
                if monkey in active:
                    raise ValueError(f'monkey in a loop: {monkey!r}')
                left, op, right = expr[monkey]
                stack.extend([(monkey, True), (left, False), (right, False)])
                active.add(monkey)
        else:
            left, op, right = expr[monkey]
            if op == '+':
                value[monkey] = value[left] + value[right]
            elif op == '-':
                value[monkey] = value[left] - value[right]
            elif op == '*':
                value[monkey] = value[left] * value[right]
            elif op == '/':
                if value[left] % value[right] != 0:
                    raise ValueError('inexact division')
                value[monkey] = value[left] // value[right]
            else:
                assert False
    return value['root']


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
