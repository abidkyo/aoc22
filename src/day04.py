#!/usr/bin/env python3

"""
Check number range overlapped condition.

x1-y1 and x2-y2

Timing:
python3 = 30 ms
"""

from aoc import map_list, read_input

# ------------------------------------------------------------------------------


def parse_range(range_str):
    """
    "2-88,13-89" => [2,88,13,89]

    1. replace "-" to ","
    2. split by ","
    3. map str to int

    """

    s = range_str.replace("-", ",").split(",")

    return map_list(int, s)


def not_overlapped(x1, y1, x2, y2):
    """
    2-4,6-8 --> 4 < 6 or 8 < 2
    """

    return y1 < x2 or y2 < x1


def overlapped(x1, y1, x2, y2):
    return not not_overlapped(x1, y1, x2, y2)


def fully_overlapped(x1, y1, x2, y2):
    """
    2-8,4-6 --> (2 <= 4 and 8 >= 6) or ( 4 <= 2 and 6 >= 8)
    """

    return (x1 <= x2 and y1 >= y2) or (x2 <= x1 and y2 >= y1)


def solve(day=4, test=False, testfile=""):
    range_list = read_input(day, test, testfile).splitlines()

    range_list = map_list(parse_range, range_list)

    # count fully overlapped range
    part1 = sum(fully_overlapped(*r) for r in range_list)

    # count (partially) overlapped range
    part2 = sum(overlapped(*r) for r in range_list)

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (2, 4)

res = solve()
assert res == (515, 883)
print(*res)

# ------------------------------------------------------------------------------
