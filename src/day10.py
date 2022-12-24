#!/usr/bin/env python3

"""
CPU cycle and CRT.

Timing:
python3 = 30 ms
"""

from aoc import read_input, print2d

# ------------------------------------------------------------------------------


def parse_instruction(txt: str):
    for line in txt:
        instr = line.split()
        if len(instr) == 1:
            yield 0
        if len(instr) == 2:
            yield from [0, int(instr[1])]


def solve(day=10, test=False, testfile=""):
    """
    Part1: Calculate signal strength.
    Part2: Draw on CRT.
    """
    txt = read_input(day, test, testfile).splitlines()
    data = parse_instruction(txt)

    # crt size is 40 * 6
    # use range because list is mutable
    crt = [[" "] * 40 for _ in range(6)]

    x = 1
    signal_strength = 0

    # cycle only goes until 240
    for cycle, instr in enumerate(data, 1):
        # 20th, 60th, 100th, 120th, ...
        if (cycle - 20) % 40 == 0:
            signal_strength += cycle * x

        row, col = divmod(cycle - 1, 40)
        if x - 1 <= col <= x + 1:
            crt[row][col] = "&"

        x += instr

    part1 = signal_strength
    part2 = crt

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res[0] == 13140

res = solve()
assert res[0] == 13440
print(res[0])
print2d(res[1])

# ------------------------------------------------------------------------------
