#!/usr/bin/env python3
#
#  Advent of Code 2024 - Day 8
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from itertools import combinations
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
        """,
        14
    ),
]

SAMPLE_CASES2 = [
    (
        """
T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
        """,
        9
    ),
    (
        """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
        """,
        34
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

EMPTY, ANTI = ".", "#"


@dataclass()
class Delta():
    dr: int
    dc: int

    def __str__(self) -> str:
        return f"({self.dr},{self.dc})"

    def __add__(self, other: Union["Pos", "Delta"]) -> Union["Pos", "Delta"]:
        if isinstance(other, Delta):
            return Delta(self.dr + other.dr, self.dc + other.dc)
        elif isinstance(other, Pos):
            return Pos(self.dr + other.row, self.dc + other.col)
        raise ValueError(f"Cannot add '{type(other)}' to Delta")

    def __sub__(self, other: "Delta") -> "Delta":
        if isinstance(other, Delta):
            return Delta(self.dr - other.dr, self.dc - other.dc)
        raise ValueError(f"Cannot subtract '{type(other)}' from Delta")


@dataclass(order=True, frozen=True)
class Pos():
    row: int
    col: int

    def __str__(self) -> str:
        return f"({self.row},{self.col})"

    def __sub__(self, other: Union["Pos", "Delta"]) -> Union["Pos", "Delta"]:
        if isinstance(other, Delta):
            return Pos(self.row - other.dr, self.col - other.dc)
        elif isinstance(other, Pos):
            return Delta(self.row - other.row, self.col - other.col)
        raise ValueError(f"Cannot subtract '{type(other)}' from Pos")

    def __add__(self, other: "Delta") -> "Pos":
        if isinstance(other, Delta):
            return Pos(self.row + other.dr, self.col + other.dc)
        raise ValueError(f"Cannot add '{type(other)}' to Pos")



@dataclass()
class Grid:
    grid: dict[Pos, str]
    nrow: Optional[int] = None
    ncol: Optional[int] = None
    nodes: Optional[dict[str, list[Pos]]] = None

    def __post_init__(self):
        self.nrow = max([pos.row for pos in self.grid.keys()]) + 1
        self.ncol = max([pos.col for pos in self.grid.keys()]) + 1

        self.nodes = defaultdict(list)
        for pos, val in self.grid.items():
            if val != EMPTY:
                self.nodes[val].append(pos)

    def on_map(self, pos) -> bool:
        return (-1 < pos.row < self.nrow) and (-1 < pos.col < self.ncol)

    def antinodes(self) -> list[Pos]:
        result: set[Pos] = set()
        for freq, locs in self.nodes.items():
            # print(f"----\n{freq}: {locs}")
            for anti in antinodes(locs):
                if self.on_map(anti):
                    result.add(anti)
        return result

    def all_antinodes(self) -> list[Pos]:
        result: set[Pos] = set()
        for freq, locs in self.nodes.items():
            # print(f"----\n{freq}: {locs}")
            for node1, node2 in combinations(locs, 2):
                result.add(node1)
                result.add(node2)

                delta = node2 - node1

                anti1 = node2 + delta
                while self.on_map(anti1):
                    result.add(anti1)
                    anti1 += delta

                anti2 = node1 - delta
                while self.on_map(anti2):
                    result.add(anti2)
                    anti2 -= delta

        return result


def parse_input(lines):
    grid = defaultdict(lambda: EMPTY)
    for row, line in enumerate(lines):
        assert line.strip()
        for col, ch in enumerate(line.strip()):
            if ch == ANTI:
                ch = EMPTY
            grid[Pos(row, col)] = ch
    return Grid(grid)

def antinodes(nodes: list[Pos]) -> list[Pos]:
    result = []
    for node1, node2 in combinations(nodes, 2):
        delta = node2 - node1
        anti1 = node2 + delta
        anti2 = node1 - delta
        result.append(anti1)
        result.append(anti2)
        # print(f"{node1}, {node2} -> {anti1}, {anti2}")
    return result


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    result = 0
    grid = parse_input(lines)
    # print(f"Loaded {grid.nrow} x {grid.ncol} grid of antennae")
    # print(grid)
    antinodes = grid.all_antinodes()
    result = len(antinodes)
    return result

def solve(lines: Lines) -> int:
    """Solve the problem."""
    result = 0
    grid = parse_input(lines)
    # print(f"Loaded {grid.nrow} x {grid.ncol} grid of antennae")
    # print(grid)
    antinodes = grid.antinodes()
    result = len(antinodes)
    return result


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
    assert result == 348
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
    assert result == 1221
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
