#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 19

>>> part1(TEST_INPUT)
33
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

from copy import deepcopy
from fractions import Fraction
from math import ceil, floor, gcd
import re
import sys
from typing import NamedTuple

TEST_INPUT = (
    "Blueprint 1: "
    "Each ore robot costs 4 ore. "
    "Each clay robot costs 2 ore. "
    "Each obsidian robot costs 3 ore and 14 clay. "
    "Each geode robot costs 2 ore and 7 obsidian."
    "\n"
    "Blueprint 2: "
    "Each ore robot costs 2 ore. "
    "Each clay robot costs 3 ore. "
    "Each obsidian robot costs 3 ore and 8 clay. "
    "Each geode robot costs 3 ore and 12 obsidian."
    "\n"
)

line_re = re.compile(
    r'Blueprint ([1-9]\d*): '
    r'Each ore robot costs ([1-9]\d*) ore. '
    r'Each clay robot costs ([1-9]\d*) ore. '
    r'Each obsidian robot costs ([1-9]\d*) ore and ([1-9]\d*) clay. '
    r'Each geode robot costs ([1-9]\d*) ore and ([1-9]\d*) obsidian.'
)


class Blueprint(NamedTuple):
    ident: int
    ore_ore: int
    clay_ore: int
    obs_ore: int
    obs_clay: int
    geode_ore: int
    geode_obs: int


def negate(row):
    for var, coeff in enumerate(row):
        row[var] = -coeff


def clear(src, dst, index):
    if src is dst:
        raise ValueError('same source and destination')
    n = len(src)
    if n != len(dst):
        raise ValueError('different row lengths')
    s = src[index]
    if s <= 0:
        raise ValueError('negative pivot')
    d = dst[index]
    for i in range(n):
        dst[i] = s*dst[i] - src[i]*d
    g = gcd(*dst)
    for i in range(n):
        dst[i] //= g


class InfeasibleLP(Exception):
    pass


class UnboundedLP(Exception):
    pass


class LinearProgram:
    def __init__(self):
        self.tableau = [[0, 1]]
        self.pivots = [1]
        self.infeasible = []

    def new_var(self):
        index = len(self.tableau[0])
        for row in self.tableau:
            row.append(0)
        return index

    def new_constraint(self, terms):
        slack = self.new_var()
        row = [0] * slack
        for coeff, var in terms:
            row[var] += coeff
        row.append(1)
        for src, index in zip(self.tableau, self.pivots):
            clear(src, row, index)
        if row[0] < 0:
            negate(row)
            row[-1] *= -1
            self.infeasible.append(slack)
        self.tableau.append(row)
        self.pivots.append(slack)

    def set_goal(self, terms):
        row = [0] * len(self.tableau[0])
        for coeff, var in terms:
            row[var] -= coeff
        row[1] = 1
        for src, index in zip(self.tableau, self.pivots):
            if index != 1:
                clear(src, row, index)
        self.tableau[0] = row

    def get_current_value(self, var):
        for row, index in zip(self.tableau, self.pivots):
            if index == var:
                return Fraction(row[0], row[index])
        return Fraction()

    def optimize(self):
        if self.infeasible:
            infeasible = self.infeasible
            original_goal = self.tableau[0]
            self.infeasible = []
            self.set_goal([(-1, var) for var in infeasible])
            if self.optimize() < 0:
                raise InfeasibleLP
            for var in infeasible:
                for row in self.tableau:
                    row[var] *= -1
            for row, index in zip(self.tableau, self.pivots):
                if row[index] < 0:
                    assert row[0] == 0
                    negate(row)
            for src, index in zip(self.tableau, self.pivots):
                if index != 1:
                    clear(src, original_goal, index)
            self.tableau[0] = original_goal

        goal = self.tableau[0]
        while True:
            could_enter = [
                var
                for var, coeff in enumerate(goal)
                if coeff < 0 and var > 1
            ]
            if not could_enter:
                break

            # choose an entering variable
            # (not very carefully)
            enter = could_enter[-1]

            could_leave = [
                (Fraction(row[0], row[enter]), index, row)
                for index, row in enumerate(self.tableau)
                if row[enter] > 0
            ]
            if not could_leave:
                raise UnboundedLP

            # this is where we could use a tie-breaker
            # for the choice of leaving variable
            _, leave, src = min(could_leave)

            self.pivots[leave] = enter
            for i, dst in enumerate(self.tableau):
                if i != leave:
                    clear(src, dst, enter)
            if not all(row[0] >= 0 for row in self.tableau[1:]):
                import pdb
                pdb.set_trace()

        return self.get_current_value(1)


def make_lp(blueprint, time=24):
    bp = blueprint
    lp = LinearProgram()
    make_geode = [lp.new_var() for _ in range(time)]
    make_obs = [lp.new_var() for _ in range(time)]
    make_clay = [lp.new_var() for _ in range(time)]
    make_ore = [lp.new_var() for _ in range(time)]
    for t in range(time):
        # factory constraint
        lp.new_constraint([
            (1, 0),
            (1, make_geode[t]),
            (1, make_obs[t]),
            (1, make_clay[t]),
            (1, make_ore[t]),
            ])
        # ore constraint
        lp.new_constraint(
            [(t+1-i, make_ore[i]) for i in range(t+1, time)]
            + [(bp.geode_ore, make_geode[i]) for i in range(t, time)]
            + [(bp.obs_ore, make_obs[i]) for i in range(t, time)]
            + [(bp.clay_ore, make_clay[i]) for i in range(t, time)]
            + [(bp.ore_ore, make_ore[i]) for i in range(t, time)]
            + [(time-t-1, 0)])
        # clay constraint
        lp.new_constraint(
            [(t+1-i, make_clay[i]) for i in range(t+1, time)]
            + [(bp.obs_clay, make_obs[i]) for i in range(t, time)])
        # obsidian constraint
        lp.new_constraint(
            [(t+1-i, make_obs[i]) for i in range(t+1, time)]
            + [(bp.geode_obs, make_geode[i]) for i in range(t, time)])
    lp.set_goal(enumerate(make_geode))
    return lp, make_geode + make_obs + make_clay + make_ore


def branch_and_bound(lp, feasible):
    stack = [lp]
    while stack:
        print(feasible, len(stack))
        lp = stack.pop()
        try:
            opt = lp.optimize()
        except InfeasibleLP:
            continue
        print(float(opt))
        if opt <= feasible:
            continue
        for row, var in zip(lp.tableau[1:], lp.pivots[1:]):
            value = Fraction(row[0], row[var])
            if value.denominator > 1:
                more = deepcopy(lp)
                more.new_constraint([(-1, var), (-ceil(value), 0)])
                less = deepcopy(lp)
                less.new_constraint([(1, var), (floor(value), 0)])
                stack.extend([less, more])
                break
        else:
            assert opt.denominator == 1
            feasible = opt.numerator


# # make a decent feasible solution
# feasible = []
# max_ore = max(bp.clay_ore, bp.obs_ore, bp.geode_ore)
# obs_bots, clay_bots, ore_bots = 0, 0, 0, 1
# obs_current = clay_current = ore_current = 0
# for t in range(time-1, 0, -1):
#     # make all relevant ore bots first
#     if ore_bots < max_ore:
#         if ore_current >= bp.ore_ore:
#             feasible.append((1, make_ore[t]))
#             ore_bots += 1
#             ore_current -= 1
#     # then prefer geode bots
#     elif (ore_current >= bp.geode_ore
#           and obs_current >= bp.geode_obs):
#         feasible.append((1, make_geode[t]))
#     # then prefer obsidian bots if relevant
#     elif (ore_current >= bp.obs_ore
#           and clay_current >= bp.obs_clay)
#           and obs_bots < bp.geode_obs):
#         feasible.append((1, make_obs[t]))
#         obs_bots += 1
#         obs_current -= 1
#     # then make clay bots if relevant
#     elif (ore_current >= bp.clay_ore
#           and clay_bots < bp.obs_clay):
#         feasible.append((1, make_clay[t]))
#         clay_bots += 1
#         clay_current -= 1
#     obs_current += obs_bots
#     clay_current += clay_bots
#     ore_current += ore_bots


def parse(line):
    m = line_re.fullmatch(line)
    if m is None:
        raise ValueError(f'bad blueprint: {line!r}')
    return Blueprint(*map(int, m.groups()))


def part1(input):
    for line in input.splitlines():
        blueprint = parse(line)
        print(max_geodes(blueprint))


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
