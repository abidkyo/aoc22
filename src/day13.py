#!/usr/bin/env python3

"""
Parse different types of data.

Timing:
python3 = 34 ms
"""

from functools import cmp_to_key
import json

from aoc import list_flatten, map_list, read_input

# ------------------------------------------------------------------------------


def compare(a, b):
    """
    = a - b
    a < b => -x
    a = b => 0
    a > b => +x
    """

    if type(a) == list and type(b) == list:
        for left, right in zip(a, b):
            if (res := compare(left, right)) != 0:
                return res
        return len(a) - len(b)

    if type(a) == list and type(b) == int:
        return compare(a, [b])

    if type(a) == int and type(b) == list:
        return compare([a], b)

    # default: a and b are int
    return a - b


def parse_packet(txt: str):
    # split line and parse with json
    return map_list(json.loads, txt.splitlines())


def solve_part1(packets):
    # Calculate the sum of index when left < right.
    return sum(idx if compare(*packet) < 0 else 0 for idx, packet in enumerate(packets, 1))


def solve_part2(packets):
    packets = packets + [[2]] + [[6]]
    packets = list_flatten(packets)

    # use 'cmp_to_key' to use comparison function
    packets = sorted(packets, key=cmp_to_key(compare))

    index_two = packets.index(2) + 1
    index_six = packets.index(6) + 1

    return index_two * index_six


def solve(day=13, test=False, testfile=""):
    txt = read_input(day, test, testfile).split("\n\n")

    packets = map_list(parse_packet, txt)

    part1 = solve_part1(packets)
    part2 = solve_part2(packets)

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (13, 140)

res = solve()
assert res == (6086, 27930)
print(*res)

# ------------------------------------------------------------------------------
