#!/usr/bin/env python3

"""
Find path of falling rocks.

Timing:
python3: ~100ms

"""

from aoc import get_digits, map_list, read_input, tuple_sum

# ------------------------------------------------------------------------------

rocks = set()
floor = 0


def parse_rocks(txt: list) -> set:
    # split line by "->", then parse digits into list
    # use () for create generator instead of list
    rock_paths = (map_list(get_digits, line.split("->")) for line in txt)

    rocks = set()
    for r in rock_paths:
        # use zip to create range from path
        for (x1, y1), (x2, y2) in zip(r[:-1], r[1:]):
            x_min, y_min = min(x1, x2), min(y1, y2)
            x_max, y_max = max(x1, x2), max(y1, y2)

            # create rock
            for x in range(x_min, x_max + 1):
                for y in range(y_min, y_max + 1):
                    rocks.add((x, y))

    return rocks


# backward simulation
def sand_pour(start, p1):
    global rocks, floor

    if start in rocks:
        # print("start", start, start[1], start[1] >= limit)
        return start[1] == floor

    # down, left, right
    for a in ((0, 1), (-1, 1), (1, 1)):
        next = tuple_sum(start, a)

        # stop if hit floor, return true
        # part2: just keep pouring until start (no return)
        if sand_pour(next, p1) and p1:
            return True

    rocks.add(start)


def solve(day=14, test=False):
    global rocks, floor

    data = read_input(day, test).splitlines()
    rocks = parse_rocks(data)

    start = (500, 0)
    floor = max(rock[1] for rock in rocks) + 2  # floor is 2 level below the lowest rock

    # add floor
    for x in range(start[0] - floor, start[0] + floor + 1):
        rocks.add((x, floor))

    rock_count = len(rocks)

    sand_pour(start, True)
    part1 = len(rocks) - rock_count

    sand_pour(start, False)
    part2 = len(rocks) - rock_count

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (24, 93)

res = solve()
print(*res)
assert res == (674, 24958)

# ------------------------------------------------------------------------------
