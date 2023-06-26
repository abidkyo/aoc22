#!/usr/bin/env python3

"""
Rock, Paper, Scissors

Result point:
    Win : 6 point
    Draw: 3 point
    Lose: 0 point

Extra point:
    Rock     : 1 point
    Paper    : 2 point
    Scissors : 3 point


Formula:
  - Move and Result are mapped to {0,1,2} respectively

    Winning Move = (Move + 1) % 3
       Draw Move = (Move + 0) % 3
     Losing Move = (Move - 1) % 3

 ->  Player Move = (Move + Result - 1) % 3
 ->       Result = (Player Move - Move + 1) % 3

Note:
  - The "Result" formula is a substitution from "Player Move" formula.
    It works because the value interval is the same ([-1,3]).
    ([ 0, 4] - 1 -> [-1, 3])
    ([-2, 2] + 1 -> [-1, 3])

Timing:
python3 = 30 ms
"""

from aoc import map_list, read_input

# ------------------------------------------------------------------------------


def parse_move(move: str):
    """
    Map string to integer {0,1,2}.

    # A;X = 0
    # B;Y = 1
    # C;Z = 2
    """

    a, _, x = move
    return [ord(a) - ord("A"), ord(x) - ord("X")]


def solve_part1(strategy: list):
    """
    Determine match result and calculate point.
    """

    points = 0
    for move in strategy:
        opponent_move, my_move = move

        res = (my_move - opponent_move + 1) % 3

        # add point for res and move
        points += res * 3
        points += my_move + 1

    return points


def solve_part2(strategy: list):
    """
    Determine move based on match result and calculate point.
    """

    points = 0
    for move in strategy:
        opponent_move, res = move

        my_move = (opponent_move + res - 1) % 3

        # add point for res and move
        points += res * 3
        points += my_move + 1

    return points


def solve(day=2, test=False):
    strategy = read_input(day, test).splitlines()

    strategy = map_list(parse_move, strategy)

    part1 = solve_part1(strategy)
    part2 = solve_part2(strategy)

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (15, 12)

res = solve()
assert res == (12645, 11756)
print(*res)

# ------------------------------------------------------------------------------
