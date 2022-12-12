#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 11

>>> part1(TEST_INPUT)
10605
>>> part2(TEST_INPUT)
2713310158
"""

from collections import namedtuple
import math
import re
import sys

TEST_INPUT = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

monkey_re = re.compile(
    r'Monkey (?P<monkey>0|[1-9]\d*):')
starting_re = re.compile(
    r'  Starting items: (?P<items>(?:0|[1-9]\d*)(?:, (?:0|[1-9]\d*))*)')
operation_re = re.compile(
    r'  Operation: new = old (?:'
    r'(?P<square>\* old)|'
    r'(?P<op>[+*]) (?P<arg>0|[1-9]\d*))')
test_re = re.compile(
    r'  Test: divisible by (?P<div>[1-9]\d*)')
true_re = re.compile(
    r'    If true: throw to monkey (?P<monkey>0|[1-9]\d*)')
false_re = re.compile(
    r'    If false: throw to monkey (?P<monkey>0|[1-9]\d*)')

Monkey = namedtuple('Monkey', 'items op div next_monkey')


def parse_next(lines, line_re):
    try:
        line = next(lines)
    except StopIteration:
        raise ValueError('missing line')
    m = line_re.fullmatch(line)
    if m is None:
        raise ValueError(f'syntax error: {line!r}')
    return m


def square(old):
    return old * old


def adder(arg):
    def op(old):
        return old + arg
    return op


def multiplier(arg):
    def op(old):
        return old * arg
    return op


operation = {
  '+': adder,
  '*': multiplier,
}


def parse(input):
    lines = iter(input.splitlines())
    monkeys = []
    while True:
        monkey = int(parse_next(lines, monkey_re)['monkey'])
        if monkey != len(monkeys):
            raise ValueError(f'wrong index: {monkey}')

        m = parse_next(lines, starting_re)
        items = [int(item) for item in m['items'].split(', ')]

        m = parse_next(lines, operation_re)
        op = square if m['square'] else operation[m['op']](int(m['arg']))

        m = parse_next(lines, test_re)
        div = int(m['div'])

        next_monkey = {
            True: int(parse_next(lines, true_re)['monkey']),
            False: int(parse_next(lines, false_re)['monkey']),
        }
        if monkey in next_monkey.values():
            raise ValueError(f'self-pass for monkey {monkey}')

        monkeys.append(Monkey(items, op, div, next_monkey))

        try:
            line = next(lines)
        except StopIteration:
            break
        if line:
            raise ValueError(f'non-blank line: {line!r}')

    return monkeys


def part1(input):
    monkeys = parse(input)
    passes = [0] * len(monkeys)
    for round in range(20):
        for monkey, (items, op, div, next_monkey) in enumerate(monkeys):
            for item in items:
                item = op(item) // 3
                monkeys[next_monkey[item % div == 0]].items.append(item)
            passes[monkey] += len(items)
            items.clear()
    passes.sort()
    return passes[-2] * passes[-1]


modulus = 0
class oomnum:
    __slots__ = ('mod', 'oomlo', 'oomhi')
    def __init__(self, mod, oomlo, oomhi):
        self.mod = mod
        self.oomlo = oomlo
        self.oomhi = oomhi
    def __add__(self, other):
        if isinstance(other, int):
            other = make_oomnum(other)
        return oomnum(
            (self.mod + other.mod) % modulus,
            max(self.oomlo, other.oomlo) + (self.oomlo == other.oomlo),
            max(self.oomhi, other.oomhi) + 1,
        )
    def __mul__(self, other):
        if isinstance(other, int):
            other = make_oomnum(other)
        return oomnum(
            (self.mod * other.mod) % modulus,
            self.oomlo + other.oomlo,
            self.oomhi + other.oomhi,
        )
    def __mod__(self, other):
        return self.mod % other
def make_oomnum(n):
    return oomnum(n % modulus, n.bit_length(), n.bit_length()+1)


def part2(input):
    monkeys = parse(input)
    global modulus; modulus = math.lcm(*(m.div for m in monkeys))
    for monkey in monkeys:
        for index, item in enumerate(monkey.items):
            monkey.items[index] = make_oomnum(item)
    passes = [0] * len(monkeys)
    for round in range(10_000):
        for monkey, (items, op, div, next_monkey) in enumerate(monkeys):
            for item in items:
                item = op(item)
                monkeys[next_monkey[item % div == 0]].items.append(item)
            passes[monkey] += len(items)
            items.clear()
    items = [i for m in monkeys for i in m.items]
    print('min', max(i.oomlo for i in items))
    print('max', max(i.oomhi for i in items))
    passes.sort()
    return passes[-2] * passes[-1]


def main(args):
    input = open('input.txt').read()
    if args == ['1']:
        print(part1(input), file=open('output1.txt', 'w'))
    elif args == ['2']:
        print(part2(input)) #, file=open('output2.txt', 'w'))
    else:
        raise ValueError(f'invalid arguments: {args!r}')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
