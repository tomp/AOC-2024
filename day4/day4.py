#!/usr/bin/env python3
#
#  Advent of Code 2024 - Day 4
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        MMMSXXMASM
        MSAMXMSMSA
        AMXSXMAAMM
        MSAMASMSMX
        XMASAMXAMM
        XXAMMXXAMA
        SMSMSASXSS
        SAXAMASAAA
        MAMMMXMMMM
        MXMXAXMASX
        """,
        18
    ),
]

SAMPLE_CASES2 = [
    (
        """
        MMMSXXMASM
        MSAMXMSMSA
        AMXSXMAAMM
        MSAMASMSMX
        XMASAMXAMM
        XXAMMXXAMA
        SMSMSASXSS
        SAXAMASAAA
        MAMMMXMMMM
        MXMXAXMASX
        """,
        9
    ),
]


Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str, strip=True, blank_lines=False) -> Lines:
    return load_text(
        Path(infile).read_text(), strip=strip, blank_lines=blank_lines
    )

def load_text(text: str, strip=True, blank_lines=False) -> Lines:
    if strip:
        lines = [line.strip() for line in text.strip("\n").split("\n")]
    else:
        lines = text.strip("\n").split("\n")
    if blank_lines:
        return lines
    return [line for line in lines if line.strip()]

def parse_sections(lines: Lines) -> Sections:
    result = []
    sect = []
    for line in lines:
        if not line.strip():
            if sect:
                result.append(sect)
            sect = []
        else:
            sect.append(line)
    if sect:
        result.append(sect)
    return result


# Solution

EMPTY = " "
XMAS = "XMAS"

DIRS = {
    "N": (-1, 0),
    "NE": (-1, 1),
    "E": (0, 1),
    "SE": (1, 1),
    "S": (1, 0),
    "SW": (1, -1),
    "W": (0, -1),
    "NW": (-1, -1),
}

@dataclass(order=True, frozen=True)
class Pos():
    row: int
    col: int

    def __str__(self) -> str:
        return f"({self.row},{self.col})"

    def neighbors(self) -> "List[Pos]":
        return [
            Pos(self.row, self.col + 1),
            Pos(self.row + 1, self.col + 1),
            Pos(self.row + 1, self.col),
            Pos(self.row + 1, self.col - 1),
            Pos(self.row, self.col - 1),
            Pos(self.row - 1, self.col - 1),
            Pos(self.row - 1, self.col),
            Pos(self.row - 1, self.col + 1),
        ]

    def neighbor(self, dir: str) -> "Pos":
        dr, dc = DIRS[dir]
        return Pos(self.row + dr, self.col + dc)


@dataclass
class Grid:
    grid: dict[Pos, str]

    def __post_init__(self):
        self.nrow = max([pos.row for pos in self.grid.keys()]) + 1
        self.ncol = max([pos.col for pos in self.grid.keys()]) + 1

    def positions(self):
        for row in range(self.nrow):
            for col in range(self.ncol):
                yield Pos(row, col)

    def matches_word(self, start: Pos, dir: str, target=XMAS) -> bool:
        result = 0
        pos = start
        for ch in target:
            if self.grid[pos] != ch:
                return False
            pos = pos.neighbor(dir)
        return True

    def matches_cross_mas(self, start: Pos) -> bool:
        if self.grid[start] != "A":
            return False

        r0, c0 = start.row, start.col

        dir1 = "NE"
        dr1, dc1 = DIRS[dir1]
        pos1, pos2 = Pos(r0+dr1,c0+dc1), Pos(r0-dr1,c0-dc1)
        if ((self.grid[pos1] == "M" and self.grid[pos2] == "S") or
            (self.grid[pos2] == "M" and self.grid[pos1] == "S")):

            dir2 = "SE"
            dr2, dc2 = DIRS[dir2]
            pos3, pos4 = Pos(r0+dr2,c0+dc2), Pos(r0-dr2,c0-dc2)
            if ((self.grid[pos3] == "M" and self.grid[pos4] == "S") or
                (self.grid[pos4] == "M" and self.grid[pos3] == "S")):

                # print(f"-> @({r0}, {c0}) \t '{self.grid[start]}'")
                # print(f"   @({pos1.row}, {pos1.col}) \t'{self.grid[pos1]}'")
                # print(f"   @({pos2.row}, {pos2.col}) \t'{self.grid[pos2]}'")
                # print(f"   @({pos3.row}, {pos3.col}) \t'{self.grid[pos3]}'")
                # print(f"   @({pos4.row}, {pos4.col}) \t'{self.grid[pos4]}'")
                # print()
                return True

        return False


    def count_words(self, target=XMAS) -> int:
        result = 0
        for pos in self.positions():
            ch = self.grid[pos]
            if ch != target[0]:
                continue
            for dir in DIRS:
                if self.matches_word(pos, dir, target):
                    result += 1
        return result

    def count_cross_words(self, target: str) -> int:
        result = 0
        for pos in self.positions():
            if self.matches_cross_mas(pos):
                result += 1
        return result


def parse_input(lines):
    grid = defaultdict(lambda: EMPTY)
    for row, line in enumerate(lines):
        assert line.strip()
        for col, ch in enumerate(line.strip()):
            grid[Pos(row, col)] = ch
    return Grid(grid)


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    target = "MAS"
    nchar = len(target)
    assert nchar % 2 == 1
    grid = parse_input(lines)
    return grid.count_cross_words(target)

def solve(lines: Lines) -> int:
    """Solve the problem."""
    grid = parse_input(lines)
    return grid.count_words()


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text)
        result = solve(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 2560
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, expected in SAMPLE_CASES2:
        lines = load_text(text)
        result = solve2(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    assert result == 1910
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
