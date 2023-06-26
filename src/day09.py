#!/usr/bin/env python3

"""
Snake.

Timing:
python3 = ~90 ms
"""

from aoc import map_list, read_input, sign

# ------------------------------------------------------------------------------


def move_snake(data: list, tail_size: int) -> set:
    V = {"R": 1, "D": -1j, "L": -1, "U": 1j}

    snake = [0] * (1 + tail_size)
    tail_pos = set()

    for direction, amount in data:
        for _ in range(int(amount)):
            snake[0] += V[direction]

            for i, tail in enumerate(snake[1:], 1):
                diff = snake[i - 1] - tail

                if abs(diff) >= 2:
                    tail += complex(sign(diff.real), sign(diff.imag))

                snake[i] = tail

            tail_pos.add(snake[-1])

    return tail_pos


def solve(day=9, test=False):
    txt = read_input(day, test).splitlines()
    data = map_list(str.split, txt)

    part1 = len(move_snake(data, 1))
    part2 = len(move_snake(data, 9))

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (13, 1)

res = solve()
print(*res)
assert res == (6406, 2643)

# ------------------------------------------------------------------------------
