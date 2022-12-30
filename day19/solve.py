#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 19

>>> bp1, bp2 = map(Blueprint.parse, TEST_INPUT.splitlines())
>>> bp1.max_geodes(24)
9
>>> bp2.max_geodes(24)
12
>>> bp1.max_geodes(32)
56
>>> bp2.max_geodes(32)
62
"""

from heapq import heappush, heappop, heapify
from itertools import combinations
from math import prod
import re
import sys
from typing import NamedTuple

TEST_INPUT = (
    "Blueprint 1: "
    "Each ore robot costs 4 ore. "
    "Each clay robot costs 2 ore. "
    "Each obsidian robot costs 3 ore and 14 clay. "
    "Each geode robot costs 2 ore and 7 obsidian.\n"
    "Blueprint 2: "
    "Each ore robot costs 2 ore. "
    "Each clay robot costs 3 ore. "
    "Each obsidian robot costs 3 ore and 8 clay. "
    "Each geode robot costs 3 ore and 12 obsidian.\n"
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
    rock_rock: int
    clay_rock: int
    obsi_rock: int
    obsi_clay: int
    geod_rock: int
    geod_obsi: int

    @classmethod
    def parse(cls, line):
        m = line_re.fullmatch(line)
        if m is None:
            raise ValueError(f'bad line: {line!r}')
        return cls(*map(int, m.groups()))

    def max_geodes(self, time):
        states = []
        initial_supplies = Supplies()
        for rock_times in self.valid_rock_times(time):
            rock_schedule = self.rock_schedule(time, rock_times)
            states.append((
                -initial_supplies.bound(self, rock_times, rock_schedule),
                initial_supplies,
                rock_times,
                rock_schedule,
            ))
        heapify(states)

        while True:
            state = heappop(states)
            bound = -state[0]
            supplies, rock_times, rock_schedule = state[1:]
            if supplies.feasible(time) == bound:
                return bound

            if supplies.clay_bots < self.obsi_clay:
                current = supplies
                while current.time < time:
                    if current.time in rock_times:
                        current = current.wait(rock_schedule)
                    elif current.can_build_clay(self):
                        current = current.wait(rock_schedule)
                        current = current.build_clay(self)
                        heappush(states, (
                            -current.bound(self, rock_times, rock_schedule),
                            current,
                            rock_times,
                            rock_schedule,
                        ))
                        break
                    else:
                        current = current.wait(rock_schedule)

            if supplies.clay_bots > 0 and supplies.obsi_bots < self.geod_obsi:
                current = supplies
                while current.time < time:
                    if current.time in rock_times:
                        current = current.wait(rock_schedule)
                    elif current.can_build_obsi(self):
                        current = current.wait(rock_schedule)
                        current = current.build_obsi(self)
                        heappush(states, (
                            -current.bound(self, rock_times, rock_schedule),
                            current,
                            rock_times,
                            rock_schedule,
                        ))
                        break
                    else:
                        current = current.wait(rock_schedule)

            if supplies.obsi_bots > 0:
                current = supplies
                while current.time < time:
                    if current.time in rock_times:
                        current = current.wait(rock_schedule)
                    elif current.can_build_geod(self):
                        current = current.wait(rock_schedule)
                        current = current.build_geod(self)
                        heappush(states, (
                            -current.bound(self, rock_times, rock_schedule),
                            current,
                            rock_times,
                            rock_schedule,
                        ))
                        break
                    else:
                        current = current.wait(rock_schedule)

    def valid_rock_times(self, time):
        max_rock = max(self.clay_rock, self.obsi_rock, self.geod_rock)
        for n in range(max_rock):
            for rock_times in combinations(range(time), n):
                if all(
                    sum(rock_times[:i]) + i <= (t - self.rock_rock) * (i+1)
                    for i, t in enumerate(rock_times)
                ):
                    yield rock_times

    def rock_schedule(self, time, rock_times):
        rs = [1] * time
        for t in rock_times:
            for i in range(t+1, time):
                rs[i] += 1
            t -= 1
            for _ in range(self.rock_rock):
                while rs[t] == 0:
                    t -= 1
                    assert t >= 0
                rs[t] -= 1
        return rs


class Supplies(NamedTuple):
    time: int = 0
    clay_bots: int = 0
    obsi_bots: int = 0
    geod_bots: int = 0
    rock: int = 0
    clay: int = 0
    obsi: int = 0
    geod: int = 0

    def wait(self, rock_schedule):
        return self._replace(
            time=self.time + 1,
            rock=self.rock + rock_schedule[self.time],
            clay=self.clay + self.clay_bots,
            obsi=self.obsi + self.obsi_bots,
            geod=self.geod + self.geod_bots,
        )

    def can_build_clay(self, bp):
        return self.rock >= bp.clay_rock

    def build_clay(self, bp):
        return self._replace(
            clay_bots=self.clay_bots + 1,
            rock=self.rock - bp.clay_rock,
        )

    def can_build_obsi(self, bp):
        return self.rock >= bp.obsi_rock and self.clay >= bp.obsi_clay

    def build_obsi(self, bp):
        return self._replace(
            obsi_bots=self.obsi_bots + 1,
            rock=self.rock - bp.obsi_rock,
            clay=self.clay - bp.obsi_clay,
        )

    def can_build_geod(self, bp):
        return self.rock >= bp.geod_rock and self.obsi >= bp.geod_obsi

    def build_geod(self, bp):
        return self._replace(
            geod_bots=self.geod_bots + 1,
            rock=self.rock - bp.geod_rock,
            obsi=self.obsi - bp.geod_obsi,
        )

    def feasible(self, time):
        return self.geod + self.geod_bots * (time - self.time)

    def bound(self, bp, rock_times, rock_schedule):
        times = range(self.time, len(rock_schedule))
        rock_schedule = rock_schedule[self.time:]

        clay_bots = self.clay_bots
        rock = self.rock
        clay_schedule = []
        for t, new_rock in zip(times, rock_schedule):
            clay_schedule.append(clay_bots)
            if rock >= bp.clay_rock and t not in rock_times:
                clay_bots += 1
                rock -= bp.clay_rock
            rock += new_rock

        obsi_bots = self.obsi_bots
        rock = self.rock
        clay = self.clay
        obsi_schedule = []
        for t, new_rock, new_clay in zip(times, rock_schedule, clay_schedule):
            obsi_schedule.append(obsi_bots)
            if (
                rock >= bp.obsi_rock
                and clay >= bp.obsi_clay
                and t not in rock_times
            ):
                obsi_bots += 1
                rock -= bp.obsi_rock
                clay -= bp.obsi_clay
            rock += new_rock
            clay += new_clay

        geod_bots = self.geod_bots
        rock = self.rock
        obsi = self.obsi
        geod = self.geod
        for t, new_rock, new_obsi in zip(times, rock_schedule, obsi_schedule):
            geod += geod_bots
            if (
                rock >= bp.geod_rock
                and obsi >= bp.geod_obsi
                and t not in rock_times
            ):
                geod_bots += 1
                rock -= bp.geod_rock
                obsi -= bp.geod_obsi
            rock += new_rock
            obsi += new_obsi
        return geod


def part1(input):
    quality = 0
    for line in input.splitlines():
        bp = Blueprint.parse(line)
        quality += bp.ident * bp.max_geodes(24)
    return quality


def part2(input):
    return prod(
        Blueprint.parse(line).max_geodes(32)
        for line in input.splitlines()[:3]
    )


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
