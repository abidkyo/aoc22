#!/usr/bin/env python3

"""
Move elements between list.

Timing:
python3 = 30 ms
"""

from aoc import get_digits, list_copy, list_remove_value, list_transpose, map_list, read_input

# ------------------------------------------------------------------------------


def parse_stacks(stacks):
    # remove numbering
    # reverse for easier parse
    stacks = stacks[:-1][::-1]

    # get all the char without bracket
    # from : ['[Z] [M] [P]', '[N] [C]', '    [D]']
    # to   : [['Z', 'M', 'P'], ['N', 'C'], [' ', 'D']]
    stacks = [list(s[1::4]) for s in stacks]

    # append space string if len of list is not enough
    # this is necessary for transpose!
    for s in stacks:
        diff = len(stacks[0]) - len(s)
        s.extend([" "] * diff)

    # transpose the stacks
    stacks = list_transpose(stacks)

    # remove space string from list
    stacks = [list_remove_value(" ", s) for s in stacks]

    # insert empty list for easier indexing
    stacks = [[""]] + stacks

    return stacks


def move_lifo(stacks, amount, source, dest):
    """Last In First Out"""
    for _ in range(amount):
        x = stacks[source].pop()
        stacks[dest].append(x)


def move_fifo(stacks, amount, source, dest):
    """First In First Out"""
    stacks[dest] += stacks[source][-amount:]
    stacks[source] = stacks[source][:-amount]


def solve(day=5, test=False):
    stacks, moves = read_input(day, test).split("\n\n")

    stacks = stacks.splitlines()
    moves = moves.splitlines()

    # parse stack
    stacks = parse_stacks(stacks)

    # copy stack for 2 use
    stacks2 = list_copy(stacks)

    # find digits in string and convert to int
    moves = map_list(get_digits, moves)

    # execute moves
    for m in moves:
        move_lifo(stacks, *m)
        move_fifo(stacks2, *m)

    # get top element (last element) in stacks and join them
    part1 = "".join(s[-1] for s in stacks)
    part2 = "".join(s[-1] for s in stacks2)

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == ("CMZ", "MCD")

res = solve()
assert res == ("WSFTMRHPP", "GSLCMFBRP")
print(*res)

# ------------------------------------------------------------------------------
