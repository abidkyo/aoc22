#!/usr/bin/env python3

"""
Move elements on the grid.

Timing:
pypy = ~7.3 s

- could be faster with complex numbers instead of tuple

"""

from collections import Counter
from itertools import count

from aoc import read_input, tuple_sum, get_neighbour

# ------------------------------------------------------------------------------


def parse_input(txt: str):
    points = set()
    for row, line in enumerate(txt):
        for col, char in enumerate(line):
            if char == "#":
                points.add((row, col))

    return points


def neighbour_at_vector(point: tuple, vector: tuple):
    """
    Example:

    vector (0,1) return [(-1,1), (0, 1), (1, 1)]
    vector (1,0) return [(1,-1), (1, 0), (1, 1)]
    """

    assert vector in list(get_neighbour(0, 0))

    for d in [-1, 0, 1]:
        if vector[0] == 0:
            yield (point[0] + d, point[1] + vector[1])
        else:
            yield (point[0] + vector[0], point[1] + d)


def get_proposal(points: set, vectors: list):
    """
    Get next move proposal.

    Propose a move if any neighbouring points are not free and
    neighbouring points at direction are free.

    You want to get away if you are close to someone,
    but you can go to a point where your left and right are free.

    points: set of occupied points
    vectors: direction vectors
    """

    pp = {}
    for p in points:
        # if any neighbouring point is in point
        if any(n in points for n in get_neighbour(*p, amount=8)):
            # try move to either NSWE, if valid
            # e.g N is valid if NE, N, NW are not in points
            for v in vectors:
                # if all neighbour at vector points are not in points
                if all(n not in points for n in neighbour_at_vector(p, v)):
                    pp[p] = tuple_sum(p, v)
                    break

    return pp


def evaluate_proposal(points: set, proposal: dict):
    """
    Move the element to proposed point
    if no other element propose the same move.
    """

    moved = False
    new_pos = set()
    pp_counter = Counter(proposal.values())

    for p in points:
        pp = proposal.get(p, None)
        if pp is None or pp_counter[pp] > 1:
            new_pos.add(p)
        else:
            new_pos.add(pp)
            moved = True

    return new_pos, moved


def calc_empty(points):
    """
    Calculate empty points on the grid bounded by the occupied points.
    """

    row = sorted(p[0] for p in points)
    col = sorted(p[1] for p in points)

    return (row[-1] - row[0] + 1) * (col[-1] - col[0] + 1) - len(points)


def solve(day=23, test=False, testfile=""):
    """
    Part1: Empty points count in 10th round.
    Part2: Nth round where no element is moving.
    """

    txt = read_input(day, test, testfile).splitlines()
    points = parse_input(txt)

    # direction vector to be considered
    # rotated for each round
    DIR = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    part1 = 0
    part2 = 0

    for cnt in count(1):
        proposal = get_proposal(points, DIR)
        points, moved = evaluate_proposal(points, proposal)

        if cnt == 10:
            part1 = calc_empty(points)

        if not moved:
            part2 = cnt
            break

        # rotate DIR
        DIR = DIR[1:] + DIR[0:1]

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (110, 20)

res = solve()
print(*res)
assert res == (4056, 999)

# ------------------------------------------------------------------------------
