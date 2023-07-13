#!/usr/bin/env python3

"""
Calculate area around points.

Note: area with 3D points; perimeter with 2D points

Timing:
python3: ~0.47s
"""

from aoc import get_digits, identity_matrix, list_flatten, map_list, read_input

# ------------------------------------------------------------------------------


def get_neighbour(point: tuple, neighbour_vector: list, lower_bound=None, upper_bound=None):
    if lower_bound is None:
        return [tuple([a + b for a, b in zip(point, n)]) for n in neighbour_vector]

    neighbour = []
    for n in neighbour_vector:
        a = tuple([a + b for a, b in zip(point, n)])
        for v in a:
            if not (lower_bound <= v <= upper_bound):
                break
        else:
            neighbour.append(a)

    return neighbour


def dfs(start: tuple, points: list, neighbour_vector: list, lower_bound: int, upper_bound: int):
    # dfs to calculate exterior area of point
    # this will only visit outside points of the existing points
    # and return them if there are adjacent to the existing points

    stack = [start]
    visited = set()

    while stack:
        p = stack.pop()

        adj = get_neighbour(p, neighbour_vector, lower_bound, upper_bound)
        for a in adj:
            if a in visited or a in points:
                continue

            stack.append(a)
            visited.add(a)

    return visited


def solve(day=18, test=False):
    data = read_input(day, test).splitlines()

    points = map_list(get_digits, data)
    length = len(points[0])  # 3 (x,y,z)

    # vector to calculate neighbouring points
    neighbour_vector = identity_matrix(length, 1) + identity_matrix(length, -1)

    # calculate lower and upper bound for dfs
    # start outside the points, so that it will not go inside (+-1 for the bound)
    lower_bound = min(list_flatten(points)) - 1
    upper_bound = max(list_flatten(points)) + 1

    exterior_points = dfs((lower_bound,) * length, points, neighbour_vector, lower_bound, upper_bound)

    area = 0
    exterior_area = 0
    for p in points:
        neighbour_points = get_neighbour(p, neighbour_vector, lower_bound - 1, upper_bound + 1)

        # part1: calculate surface area of points (cubic)
        area += sum(a not in points for a in neighbour_points)

        # part2: calculate only exterior surface area of points
        # note: it is easier to calculate the exterior area,
        # instead of finding a hole in the grid and subtract that from the calculated area
        exterior_area += sum(a in exterior_points for a in neighbour_points)

    return area, exterior_area


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (64, 58)

res = solve()
print(*res)
assert res == (3586, 2072)

# ------------------------------------------------------------------------------
