#!/usr/bin/env python3

"""
Find common character in strings.

Points:
    lowercase: 1 - 26
    uppercase: 27 - 52

Timing:
python3 = 30 ms
"""

from aoc import read_input

# ------------------------------------------------------------------------------


def char_point(char: str):
    if char.islower():
        return ord(char) - ord("a") + 1
    elif char.isupper():
        return ord(char) - ord("A") + 27


def solve_part1(strings: list):
    """
    Find common char in two part of a string
    and calculate points.
    """

    points = 0
    for s in strings:
        half = len(s) // 2

        a = set(s[:half])
        b = set(s[half:])

        # just pop because we know there is only one common char
        char = (a & b).pop()
        points += char_point(char)

    return points


def solve_part2(strings: list):
    """
    Find common char in three strings
    and calculate points.
    """

    points = 0
    for idx in range(0, len(strings), 3):
        a = set(strings[idx])
        b = set(strings[idx + 1])
        c = set(strings[idx + 2])

        # just pop because we know there is only one common char
        char = (a & b & c).pop()
        points += char_point(char)

    return points


def solve(day=3, test=False, testfile=""):
    txt = read_input(day, test, testfile).splitlines()

    part1 = solve_part1(txt)
    part2 = solve_part2(txt)

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (157, 70)

res = solve()
assert res == (7428, 2650)
print(*res)

# ------------------------------------------------------------------------------
