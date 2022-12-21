#!/usr/bin/env python3

"""
Find bigger element in matrix.

Timing:
python3 = 83 ms
"""

from itertools import product
from math import prod
from aoc import infinity, integers, list_transpose, map_list, read_input

# ------------------------------------------------------------------------------


def get_bigger_idxs(direction: list, element: int):
    # return generator, idx of first bigger element or infinity value
    # start from 1 because element is not included in d
    return next((idx for idx, val in enumerate(direction, 1) if val >= element), infinity)


def solve(day=8, test=False, testfile=""):
    txt = read_input(day, test, testfile).splitlines()

    # create matrix from the txt
    forest = map_list(integers, txt)
    forestT = list_transpose(forest)

    # forest is square
    forest_width = len(forest[0])

    bigger_count = 0
    highest_score = 0
    for x, y in product(range(1, forest_width - 1), repeat=2):
        element = forest[x][y]
        row = forest[x]
        column = forestT[y]

        # above, right, below, left
        # flip the array for distance calculation
        directions = (
            column[:x][::-1],
            row[:y][::-1],
            column[x + 1 :],
            row[y + 1 :],
        )

        bigger_idxs = [get_bigger_idxs(d, element) for d in directions]
        bigger_count += any(idx == infinity for idx in bigger_idxs)

        # note: square bracket for list, parentheses for iterable
        score = [min(idx, len(d)) for idx, d in zip(bigger_idxs, directions)]
        highest_score = max(highest_score, prod(score))

    # bigger element count + outer element count
    part1 = bigger_count + (len(forest) + len(forest) - 2) * 2
    part2 = highest_score

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (21, 8)

res = solve()
assert res == (1693, 422059)
print(*res)

# ------------------------------------------------------------------------------
