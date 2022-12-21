#!/usr/bin/env python3

"""
Calculate sum of numbers represented as string.

Timing:
python3 = 30 ms
"""

from aoc import read_input

# ------------------------------------------------------------------------------


def solve(day=1, test=False, testfile=""):
    # split by blank line to get section
    sections = read_input(day, test, testfile).split("\n\n")

    # calc sum for each section
    total = []
    for section in sections:
        values = section.splitlines()

        # convert string to int and calculate sum
        total.append(sum(map(int, values)))

    # part1: get max section value
    part1 = max(total)

    # part2: calculate sum of top three section.
    part2 = sum(sorted(total)[-3:])

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (24000, 45000)

res = solve()
assert res == (69310, 206104)
print(*res)

# ------------------------------------------------------------------------------
