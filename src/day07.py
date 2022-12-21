#!/usr/bin/env python3

"""
Traverse file system and calculate directory size.

Timing:
python3 = 35 ms
"""

from __future__ import annotations
from dataclasses import dataclass, field

from aoc import read_input

# ------------------------------------------------------------------------------


@dataclass(frozen=True)
class File:
    name: str
    size: int


@dataclass
class Directory:
    name: str
    parent: Directory
    subdir: dict = field(default_factory=dict)
    files: list = field(default_factory=list)

    def add_file(self, filename: str, filesize: int) -> None:
        file = File(filename, filesize)
        self.files.append(file)

    def add_subdir(self, dirname: str) -> None:
        dir = Directory(dirname, self)
        self.subdir[dirname] = dir

    def get_directory_size(self, size_list: list) -> int:
        # calculate file and dir size recursively
        file_size = sum(file.size for file in self.files)
        dir_size = sum(dir.get_directory_size(size_list) for dir in self.subdir.values())

        # calculate total size and append to list
        size = dir_size + file_size
        size_list.append(size)

        return size


# ------------------------------------------------------------------------------


def parse_content(content: list) -> Directory:
    root = Directory("root", None)

    current_dir = root
    for line in content:
        token = line.split()

        # $ cd ..
        # $ cd xxx
        # $ cd / (ignored)
        if len(token) == 3:
            if token[2] == "..":
                # change to parent directory if available
                current_dir = current_dir.parent if current_dir.parent else current_dir
            elif token[2].isalpha():
                # create new subdirectory
                current_dir = current_dir.subdir[token[2]]

        # dir xxx
        # 134 xxx
        # $ ls (ignored)
        elif len(token) == 2:
            if token[0] == "dir":
                # add subdirectory of the directory
                current_dir.add_subdir(token[1])
            elif token[0].isnumeric():
                # add file of the directory
                current_dir.add_file(token[1], int(token[0]))

    return root


def solve(day=7, test=False, testfile=""):
    content = read_input(day, test, testfile).splitlines()

    root = parse_content(content)

    # calculate directory size for every directory
    dir_size = []
    root_size = root.get_directory_size(dir_size)

    # total directory size of directory size lower than 100k
    part1 = sum(s for s in dir_size if s <= 100_000)

    # find a directory and its size to be deleted so that unused space is 30M of 70M
    limit = root_size - 40_000_000  # 30M - 70M
    part2 = min(s for s in dir_size if limit <= s)

    return part1, part2


# ------------------------------------------------------------------------------

# res = solve(test=True)
# assert res == (95437, 24933642)

res = solve()
assert res == (1611443, 2086088)
print(*res)

# ------------------------------------------------------------------------------
