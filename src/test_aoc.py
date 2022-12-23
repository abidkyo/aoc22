#!/usr/bin/env python3

"""
Test Function for AOC.
"""

from aoc import get_neighbour


def testNeighbour():
    """Test neighbour for point (0,0)."""
    # 4-neighbour NSWE
    V4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    n4 = list(get_neighbour(0, 0, 4))
    assert len(n4) == len(V4)
    assert all(n in V4 for n in n4)

    # 8-neighbour NW, N, NE, W, E, SW, S, SE
    V8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    n8 = list(get_neighbour(0, 0, 8))
    assert len(n8) == len(V8)
    assert all(n in V8 for n in n8)

    # 9-neighbour NW, N, NE, W, E, SW, S, SE
    V9 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
    n9 = list(get_neighbour(0, 0, 9))
    assert len(n9) == len(V9)
    assert all(n in V9 for n in n9)
