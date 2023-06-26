#!/usr/bin/env python3

"""
Get index of char, where previous n-chars are different.

Timing:
python3 = 30 ms
"""

from aoc import read_input

# ------------------------------------------------------------------------------


def find_distinct_chars(string: str, n: int):
    """
    Find the first distinct n-characters inside the string.

    return: idx of the last character
    """
    for idx in range(n, len(string)):
        chars = string[(idx - n) : idx]
        if len(set(chars)) == len(chars):
            return idx


def solve(day=6, test=False):
    string = read_input(day, test)

    part1 = find_distinct_chars(string, 4)
    part2 = find_distinct_chars(string, 14)

    return part1, part2


# ------------------------------------------------------------------------------

# strings = [
#     "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
#     "bvwbjplbgvbhsrlpgdmjqwftvncz",
#     "nppdvjthqldpwncqszvftbrmjlhg",
#     "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
#     "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
# ]

# idxs4 = [7, 5, 6, 10, 11]
# idxs14 = [19, 23, 23, 29, 26]

# for string, idx4, idx14 in zip(strings, idxs4, idxs14):
#     i = find_distinct_chars(string, 4)
#     assert i == idx4

#     i = find_distinct_chars(string, 14)
#     assert i == idx14


res = solve()
assert res == (1109, 3965)
print(*res)

# ------------------------------------------------------------------------------
