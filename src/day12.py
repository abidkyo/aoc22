#!/usr/bin/env python3

"""
Find shortest path.

Timing:
python3 : ~0.75s

"""

from aoc import get_neighbour, read_input

# ------------------------------------------------------------------------------


def parse_grid(data: str):
    grid = {}
    for y in range(len(data)):
        for x in range(len(data[0])):
            char = data[y][x]

            if char == "E":
                end, char = (x, y), "z"
            elif char == "S":
                start, char = (x, y), "a"

            grid[x, y] = char

    return grid, start, end


def valid_neighbour(g, x, y, p2):
    if not p2:
        return (z for z in get_neighbour(x, y) if z in g and ord(g[z]) - ord(g[x, y]) <= 1)
    else:
        return (z for z in get_neighbour(x, y) if z in g and ord(g[x, y]) - ord(g[z]) <= 1)


# bfs for shortest path problem
def bfs(grid, start, end, p2=False):
    stack = [(0, start)]
    seen = {start: 0}

    while stack:
        steps, (x, y) = stack.pop(0)

        if (x, y) == end if not p2 else grid[x, y] == "a":
            return steps

        next_steps = steps + 1

        for z in valid_neighbour(grid, x, y, p2):
            # avoid returning to previous seen point
            if seen.get(z, None) is not None:
                continue

            seen[z] = next_steps
            stack.append((next_steps, z))


def solve(day=12, test=False):
    data = read_input(day, test).splitlines()

    grid, start, end = parse_grid(data)

    # find shortest path from "S" to "E" (ascending)
    part1 = bfs(grid, start, end)

    # find shortest path from "E" to any "a" (descending)
    part2 = bfs(grid, end, start, True)

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (31, 29)

res = solve()
print(*res)
assert res == (517, 512)

# ------------------------------------------------------------------------------
