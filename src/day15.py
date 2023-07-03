#!/usr/bin/env python3

"""
Manhattan distance and range.

Timing:
python3: ~6.40s
pypy: ~3.65s

"""

from aoc import get_digits, manhattan_distance, map_list, read_input

# ------------------------------------------------------------------------------


def parse_positions(string: str) -> tuple:
    # get coordinate of sensor and beacon
    sx, sy, bx, by = get_digits(string)

    # calculate manhattan distance
    distance = manhattan_distance((sx, sy), (bx, by))

    # return sensor position and 'radius' of area covered
    return (sx, sy), distance


def find_edges_at_row(sensors: list, row: int) -> list:
    # in this case, manhattan distance is the radius
    # find the left- and right-edges of the 'circle' on that row

    edges = set()
    for (sx, sy), r in sensors:
        # calculate number of points covered by the sensor in the row (line segment length)
        points = r - abs(sy - row)

        # if the area covered by the sensor intercept that row,
        # store the left- and right-edge x-coordinate (edge range)
        if points >= 0:
            edges.add((sx - points, sx + points))

    # return the edges sorted in ascending order
    # this will only sort by the left-edge values
    return sorted(edges)


def find_gap(edges: list) -> int:
    # find the gap in area covered by the sensors (range is not overlapping)
    # only need to track the right-edge value since 'edges' is sorted

    most_right = 0
    for left, right in edges:
        # a gap has diff of more than 1
        if (left - most_right) > 1:
            # return the gap position (+1)
            return most_right + 1
        else:
            most_right = max(right, most_right)

    # return -1 if no gap is found
    return -1


def solve_part1(sensors: list, row: int) -> int:
    """
    Find the number of points that CANNOT contain a beacon in a specific row.
    """

    edges = find_edges_at_row(sensors, row)

    # get the min left-edge and max right-edge values
    leftx, _ = edges[0]  # this should be fine because 'edges' is sorted
    _, rightx = max(edges, key=lambda x: x[1])

    # subtract to get the number of point covered
    num_point = rightx - leftx

    return num_point


def solve_part2(sensors: list, limit: int):
    """
    Find the location of the beacon that is not detected by the sensors.
    This is indicated by the gap, which is the point, where the edges range is not overlapped.

    Return the tuning frequency which is x * 4_000_000 + y.
    """

    # start from the bottom should be faster
    for row in reversed(range(limit + 1)):
        edges = find_edges_at_row(sensors, row)

        # if a gap is found, return the tuning frequency
        if (gap := find_gap(edges)) != -1:
            return gap * 4_000_000 + row


def solve(day=15, test=False):
    data = read_input(day, test).splitlines()

    sensors = map_list(parse_positions, data)

    limit = 20 if test else 4_000_000
    part1 = solve_part1(sensors, limit // 2)
    part2 = solve_part2(sensors, limit)

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (26, 56_000_011)

res = solve()
print(*res)
assert res == (4_793_062, 10_826_395_253_551)

# ------------------------------------------------------------------------------
