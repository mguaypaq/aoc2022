#!/usr/bin/python3
"""
Advent of Code 2022 -- Day 16

>>> part1(TEST_INPUT)
1651
>>> part2(TEST_INPUT)
Traceback (most recent call last):
...
NotImplementedError
"""

import re
import sys
from typing import NamedTuple

TEST_INPUT = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""

# this regular expression is very pedantic: it checks the grammar
line_re = re.compile(
    r'Valve (?P<name>[A-Z]{2}) '
    r'has flow rate=(?P<rate>0|[1-9]\d*); '
    r'tunnel(?P<plural>s)? lead(?(plural)|s) to valve(?(plural)s) '
    r'(?P<neighbours>[A-Z]{2}(?(plural)(?:, [A-Z]{2})+))'
)


class Valve(NamedTuple):
    name: str
    rate: int
    neighbours: list[str]


class State(NamedTuple):
    name: str
    opened: list[str]
    released: int
    time: int

    def next_states(self, valves, costs):
        name, opened, released, time = self
        for n in costs.keys() - opened:
            after = time - costs[n][name]
            if after > 0:
                yield State(
                    name=n,
                    opened=opened + [n],
                    released=released + after * valves[n].rate,
                    time=after,
                )

    def bound(self, valves, costs):
        name, opened, released, time = self
        for n in costs.keys() - opened:
            after = time - costs[n][name]
            if after > 0:
                released += after * valves[n].rate
        return released

    def feasible(self, valves, costs):
        name, opened, released, time = self
        heuristic = sorted(
            costs.keys() - opened,
            key=lambda n: valves[n].rate,
            reverse=True,
        )
        for n in heuristic:
            after = time - costs[n][name]
            if after > 0:
                name = n
                released += after * valves[n].rate
                time = after
        return released


def parse(input):
    valves = {}
    for line in input.splitlines():
        m = line_re.fullmatch(line)
        if m is None:
            raise ValueError(f'bad line: {line!r}')
        name = m['name']
        if name in valves:
            raise ValueError(f'duplicate valve: {name}')
        valves[name] = Valve(
            name=name,
            rate=int(m['rate']),
            neighbours=m['neighbours'].split(', '),
        )
    for src in valves:
        for dst in valves[src].neighbours:
            if src not in valves[dst].neighbours:
                raise ValueError(f'one-way tunnel from {src} to {dst}')
    return valves


def time_cost(valves, destination):
    result = {}
    queue, cost = [destination], 1
    while queue:
        next_queue = []
        for name in queue:
            if name not in result:
                result[name] = cost
                next_queue.extend(valves[name].neighbours)
        queue, cost = next_queue, cost+1
    return result


def part1(input):
    valves = parse(input)
    costs = {
        name: time_cost(valves, name)
        for name in valves
        if valves[name].rate > 0
    }

    best = 0
    stack = [State(
        name='AA',
        opened=[],
        released=0,
        time=30,
    )]
    while stack:
        state = stack.pop()
        if state.bound(valves, costs) > best:
            best = max(best, state.feasible(valves, costs))
            stack.extend(state.next_states(valves, costs))
    return best


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
