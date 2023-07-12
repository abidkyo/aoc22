#!/usr/bin/env python3

"""
Find maximum value.

Timing
python3: ~11.8s
pypy: ~8.2s
"""

from functools import lru_cache
from itertools import product
import re

from aoc import infinity, get_digits, map_list, read_input

# ------------------------------------------------------------------------------


paths = {}


def parse_input(txt: list):
    valves = []
    paths = {}

    for line in txt:
        names = map_list(str, re.findall(r"[A-Z]{2}", line))
        rate = get_digits(line)[-1]

        origin = names[0]

        valves.append((origin, rate))

        paths[origin] = {}

        # store length from origin to destination; always 1
        for dest in names[1:]:
            paths[origin][dest] = 1

    return valves, paths


def floyd_warshall(valves):
    """
    Calculate shortest path of all traversable paths using Floyd-Warshall algorithm.
    """

    global paths

    names = [v[0] for v in valves]

    # loop through all cartesian product
    for k, i, j in product(names, names, names):
        # continue if path to self
        if i == j or j == k or i == k:
            continue

        ij = paths[i].get(j, infinity)
        ik = paths[i].get(k, None)
        kj = paths[k].get(j, None)

        # continue if path blocked
        if ik is None or kj is None:
            continue

        # add ij path to paths
        if ij > ik + kj:
            ij = ik + kj
            paths[i][j] = ij


@lru_cache(maxsize=None)
def dfs(start, choices, time_left, p2=False):
    global paths

    res = {}
    for i in range(len(choices)):
        chosen, rest = choices[i], tuple(choices[:i] + choices[i + 1 :])
        dest, rate = chosen

        distance = paths[start].get(dest, infinity)
        t = time_left - distance - 1

        if t <= 0:
            continue

        path, flow = dfs(dest, rest, t, p2)
        res[start + "->" + path] = rate * t + flow

    if p2:
        path, flow = dfs("AA", choices, 26, False)
        res[start + "->" + "human" + "->" + path] = flow

    if not res:
        return start, 0

    k = max(res, key=res.get)
    return k, res[k]


def solve(day=16, test=False):
    global paths

    data = read_input(day, test).splitlines()

    valves, paths = parse_input(data)
    floyd_warshall(valves)

    # filter valves with flowrate > 0
    valves = tuple(filter(lambda x: x[1] > 0, valves))

    START = "AA"

    time_left = 30
    part1 = dfs(START, valves, time_left)

    time_left = 26
    part2 = dfs(START, valves, time_left, True)

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# print(*res)
# assert (res[0][1], res[1][1]) == (1651, 1707)

res = solve()
print(*res)
assert (res[0][1], res[1][1]) == (1559, 2191)

# ------------------------------------------------------------------------------
