#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 21

>>> part1(TEST_INPUT)
152
>>> part2(TEST_INPUT)
301
"""

import itertools as it
import re
import sys
from typing import Iterable

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


class Polynomial:
    def __init__(self, coeffs: Iterable[int]):
        coeffs = list(coeffs)
        while coeffs and coeffs[-1] == 0:
            coeffs.pop()
        self.coeffs = coeffs

    def __len__(self):
        return len(self.coeffs)

    def __iter__(self):
        return iter(self.coeffs)

    def __add__(self, other):
        return Polynomial(
            a + b for a, b in it.zip_longest(self, other, fillvalue=0)
        )

    def __sub__(self, other):
        return Polynomial(
            a - b for a, b in it.zip_longest(self, other, fillvalue=0)
        )

    def __lshift__(self, count):
        return Polynomial([0] * count + self.coeffs)

    def scale(self, scalar):
        return Polynomial(a * scalar for a in self)

    def __mul__(self, other):
        return sum((
            self.scale(coeff) << degree
            for degree, coeff in enumerate(other)
        ), start=Polynomial([]))


class Rational:
    def __init__(self, numerator, denominator):
        self.num = numerator
        self.den = denominator

    def __add__(self, other):
        return Rational(
            self.num * other.den + self.den * other.num,
            self.den * other.den,
        )

    def __sub__(self, other):
        return Rational(
            self.num * other.den - self.den * other.num,
            self.den * other.den,
        )

    def __mul__(self, other):
        return Rational(
            self.num * other.num,
            self.den * other.den,
        )

    def __truediv__(self, other):
        return Rational(
            self.num * other.den,
            self.den * other.num,
        )

    def __mod__(self, other):
        return 0

    def __floordiv__(self, other):
        return self / other


def parse(input):
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
    return value, expr


def compute(value, expr, monkeys):
    stack = [(m, False) for m in monkeys]
    active = set()
    while stack:
        monkey, ready = stack.pop()
        if not ready:
            if monkey not in value:
                if monkey in active:
                    raise ValueError(f'monkey in a loop: {monkey!r}')
                left, _, right = expr[monkey]
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


def part1(input):
    value, expr = parse(input)
    compute(value, expr, ['root'])
    return value['root']


def part2(input):
    value, expr = parse(input)
    rational = {
        m: Rational(Polynomial([v]), Polynomial([1]))
        for m, v in value.items()
    }
    rational['humn'] = Rational(Polynomial([0, 1]), Polynomial([1]))
    left, _, right = expr['root']
    compute(rational, expr, [left, right])
    poly = (rational[left] - rational[right]).num
    if len(poly) == 2:
        b, a = poly
        if b % a != 0:
            raise ValueError('rational solution')
        return -b // a
    else:
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
