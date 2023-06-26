#!/usr/bin/env python3

"""
Move elements between list.

Timing:
python3 : ~9.63s

old:
act : 4.883

"""

from dataclasses import dataclass
from math import prod

from aoc import list_copy, map_list, read_input, get_digits

# ------------------------------------------------------------------------------


@dataclass
class Monkey:
    items: list
    oper: str
    test: int
    true: int
    false: int
    counter: int


def parse_monkey(txt: str):
    txt = txt.splitlines()

    return Monkey(
        list(get_digits(txt[1])),
        txt[2].split(":")[-1].replace(" new = ", "lambda old: "),
        get_digits(txt[3])[-1],
        get_digits(txt[4])[-1],
        get_digits(txt[5])[-1],
        0,
    )


def execute_round(monkeys: Monkey, part2: bool = False, mod: int = 1):
    for m in monkeys:
        # increase item counter
        m.counter += len(m.items)

        for item in m.items:
            if part2:
                new = eval(m.oper)(item) % mod
            else:
                new = eval(m.oper)(item) // 3

            dest = m.true if new % m.test == 0 else m.false
            monkeys[dest].items.append(new)

        m.items = []


def solve(day=11, test=False, testfile=""):
    txt = read_input(day, test).split("\n\n")

    m1 = map_list(parse_monkey, txt)
    m2 = list_copy(m1)

    # calculate modulo for part 2
    # use modulo to scale down number
    mod = prod(m.test for m in m2)

    # part1
    for _ in range(20):
        execute_round(m1)

    # part2
    for _ in range(10000):
        execute_round(m2, True, mod)

    part1 = prod(sorted(m.counter for m in m1)[-2:])
    part2 = prod(sorted(m.counter for m in m2)[-2:])

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (10605, 2713310158)

res = solve()
print(*res)
assert res == (117640, 30616425600)

# ------------------------------------------------------------------------------
