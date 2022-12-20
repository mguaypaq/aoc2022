#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 19

# too slow:
# >>> part1(TEST_INPUT)
# 33
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

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

infty = float('inf')


class Blueprint(NamedTuple):
    ident: int
    ore_ore: int
    clay_ore: int
    obs_ore: int
    obs_clay: int
    geode_ore: int
    geode_obs: int


class State(NamedTuple):
    ore_robot: int = 1
    clay_robot: int = 0
    obs_robot: int = 0
    geode_robot: int = 0
    ore: int | float = 0
    clay: int | float = 0
    obs: int | float = 0
    geode: int = 0

    def __le__(self, other):
        return all(s <= o for s, o in zip(self, other))

    def __lt__(self, other):
        return self != other and self <= other

    def successors(self, bp):
        (ore_robot, clay_robot, obs_robot, geode_robot,
            old_ore, old_clay, old_obs, geode) = self

        max_ore = max(bp.ore_ore, bp.clay_ore, bp.obs_ore, bp.geode_ore)
        ore = old_ore + ore_robot if ore_robot < max_ore else infty
        clay = old_clay + clay_robot if clay_robot < bp.obs_clay else infty
        obs = old_obs + obs_robot if obs_robot < bp.geode_obs else infty
        geode += geode_robot

        yield State(
            ore_robot, clay_robot, obs_robot, geode_robot,
            ore, clay, obs, geode,
        )
        if ore < infty and bp.ore_ore <= old_ore:
            yield State(
                ore_robot + 1, clay_robot, obs_robot, geode_robot,
                ore - bp.ore_ore, clay, obs, geode,
            )
        if clay < infty and bp.clay_ore <= old_ore:
            yield State(
                ore_robot, clay_robot + 1, obs_robot, geode_robot,
                ore - bp.clay_ore, clay, obs, geode,
            )
        if obs < infty and bp.obs_ore <= old_ore and bp.obs_clay <= old_clay:
            yield State(
                ore_robot, clay_robot, obs_robot + 1, geode_robot,
                ore - bp.obs_ore, clay - bp.obs_clay, obs, geode,
            )
        if bp.geode_ore <= old_ore and bp.geode_obs <= old_obs:
            yield State(
                ore_robot, clay_robot, obs_robot, geode_robot + 1,
                ore - bp.geode_ore, clay, obs - bp.geode_obs, geode,
            )


def part1(input):
    quality = 0
    for line in input.splitlines():
        m = line_re.fullmatch(line)
        if m is None:
            raise ValueError(f'bad line: {line!r}')
        bp = Blueprint(*map(int, m.groups()))
        states = {State()}
        for _ in range(24):
            new_states = set()
            for s in states:
                new_states.update(s.successors(bp))
            states = {
                s for s in new_states
                if not any(s < t for t in new_states)
            }
        quality += bp.ident * max(s.geode for s in states)
    return quality


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
