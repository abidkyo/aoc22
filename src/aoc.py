#!/usr/bin/env python3

"""
Helper Function for AOC.
"""


from itertools import chain, repeat, islice, product
from copy import deepcopy
import math
import re


infinity = float("inf")


def map_tuple(type, iterable):
    return tuple(map(type, iterable))


def map_list(type, iterable):
    return list(map(type, iterable))


def identity_matrix(n: int, val: int = 1):
    mat = []
    for i in range(n):
        mat.append([])
        for j in range(n):
            if i == j:
                mat[i].append(val)
            else:
                mat[i].append(0)

    return mat


def get_neighbour(x, y, amount=4):
    assert amount in {4, 8, 9}

    for dx, dy in product([-1, 0, 1], repeat=2):
        if (amount == 4 and abs(dx) != abs(dy)) or (amount == 8 and not dx == dy == 0) or (amount == 9):
            yield (x + dx, y + dy)


# todo: testfile name is unnecessary
def read_input(day: int, test: bool, testfile: str) -> str:
    # filename = "input/day01.txt"
    # filename = "input/day01_test.txt"
    # filename = "input/day01_test1.txt"
    filename = f"input/day{day:02d}"
    filename += f"_test{testfile}" if test else ""
    filename += ".txt"

    with open(filename, "r") as f:
        return f.read()


def integers(string: str) -> list:
    return map_list(int, string)


def get_digits(string: str) -> list:
    return map_tuple(int, re.findall(r"-?\d+", string))


def manhattan_distance(x: tuple, y: tuple) -> int:
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def euclidean_distance(x: tuple, y: tuple) -> int:
    return math.sqrt(abs(x[0] - y[0]) ** 2 + abs(x[1] - y[1]) ** 2 + abs(x[2] - y[2]) ** 2)


def tuple_sum(a: tuple, b: tuple) -> tuple:
    return tuple(sum([x, y]) for x, y in zip(a, b))


def iter_take(n: int, iterable) -> list:
    # return next item from generator or None for n-times
    return list(islice(iterable, n))


def iter_ncycles(n, iterable):
    return chain.from_iterable(repeat(iterable, n))


def list_flatten(iterable):
    return chain.from_iterable(iterable)


def list_transpose(src: list) -> list:
    # length of every list should be the same
    assert all(len(a) == len(src[0]) for a in src)

    return map_list(list, zip(*src))


def list_copy(src: list) -> list:
    # every other method of copy
    # does not actually copy the list
    return deepcopy(src)


def list_remove_value(val, src: list) -> list:
    return list(filter(lambda x: x != val, src))
