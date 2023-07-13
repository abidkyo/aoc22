#!/usr/bin/env python3

"""
Tetris and Cache.

Timing:
python3: ~5.36s
pypy: ~2.07s
"""

from itertools import cycle

from aoc import iter_take, read_input

# ------------------------------------------------------------------------------


def visualize(grid: list):
    import numpy as np

    height = max(int(x.imag) for x in grid) + 1 + 3
    width = 7

    data = np.full((height, width), ".", str)

    for z in grid:
        x, y = int(z.real), int(z.imag)

        data[(y, x)] = "#"

    print()
    print(np.flip(data, 0))
    print()


def get_rock_data():
    rock_shape = ["####", ".#.\n###\n.#.", "..#\n..#\n###", "#\n#\n#\n#", "##\n##"]

    rocks = []
    for shape in rock_shape:
        # reverse the layout
        shape = shape.splitlines()[::-1]

        # store position of rock
        # rock spawn 2 units from the left
        # rock end up 1 unit above the highest rock point
        rock = [complex(x, y) for y, s in enumerate(shape, 1) for x, c in enumerate(s, 2) if c == "#"]
        rocks.append(sorted(rock, key=lambda x: x.real))

    return rocks


def get_gas_direction(txt: str):
    return [1 if char == ">" else -1 for char in txt]


def floor_hit(pos, floor):
    # if hit floor
    return True if (set(pos) & set(floor)) else False


def wall_hit(pos):
    # if hit left or right side
    a = sorted([int(x.real) for x in pos])
    return a[0] < 0 or a[-1] > 6


def move_rock(pos, d, floor):
    new_pos = [p + d for p in pos]

    if floor_hit(new_pos, floor) or wall_hit(new_pos):
        return pos

    return new_pos


def spawn_move(pos, dir, floor_height):
    # spawn and make 4 horizontal move, and bring to floor level
    left, right = pos[0].real, pos[-1].real

    diff = 0
    for d in dir:
        x1 = left + d
        x2 = right + d
        if x1 < 0 or x2 > 6:
            continue

        left += d
        right += d
        diff += d

    return [p + complex(diff, floor_height) for p in pos]


def solve(day=17, test=False):
    data = read_input(day, test).strip()

    rocks = get_rock_data()
    rocks = cycle(((idx, pos) for idx, pos in enumerate(rocks)))

    directions = get_gas_direction(data)
    directions = cycle(((idx, direction) for idx, direction in enumerate(directions)))

    floor = set(complex(i, 0) for i in range(7))

    limit_p1 = 2022
    limit_p2 = 1_000_000_000_000

    rock_count = 0
    floor_height = 0
    top_layout = [0] * 7

    height_leap = 0

    # allow cache to be used only once
    cache_used = False
    cache = {}

    while True:
        if rock_count == limit_p2:
            break

        if rock_count == limit_p1:
            part1 = floor_height

        rock_count += 1

        curr_rockidx, curr_rock = next(rocks)
        curr_gasidx, curr_gas = tuple(zip(*iter_take(4, directions)))
        curr_gasidx = curr_gasidx[0]

        # cache implementation
        # key: curr_rockidx, curr_gasidx, top_layout
        # val: floor_height, rock_count
        # so when same key is found
        # we can find the floor height increased and rock count increased since last time
        # multiplier = (rock limit - rock count) // diff rock count
        # then height leap = increased floor height * mult
        # then current rock count += increased rock count * mult
        if not cache_used and rock_count > limit_p1:
            # lower the number of top layout by subtraction
            top = tuple(floor_height - y for y in top_layout)
            cache_key = curr_rockidx, curr_gasidx, top

            if cache_key not in cache:
                cache[cache_key] = (floor_height, rock_count)
            else:
                old_height, old_count = cache[cache_key]

                height_diff = floor_height - old_height
                count_diff = rock_count - old_count

                multi = (limit_p2 - rock_count) // count_diff

                height_leap = height_diff * multi
                rock_count += count_diff * multi

                cache_used = True

        curr_pos = spawn_move(curr_rock, curr_gas, floor_height)

        while True:
            # try move below
            next_pos = move_rock(curr_pos, complex(0, -1), floor)

            # check if pos changed
            if next_pos == curr_pos:
                break

            # if yes, update pos
            curr_pos = next_pos

            # move horizontal
            _, curr_gas = next(directions)
            curr_pos = move_rock(curr_pos, complex(curr_gas, 0), floor)

        # update height
        floor_height = max([int(x.imag) for x in curr_pos] + [floor_height])

        # update top layout
        for z in curr_pos:
            x, y = int(z.real), int(z.imag)
            top_layout[x] = y

        # add rock pos to floor
        floor.update(curr_pos)

    part2 = floor_height + height_leap

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (3068, 1514285714288)

res = solve()
print(*res)
assert res == (3179, 1567723342929)

# ------------------------------------------------------------------------------
