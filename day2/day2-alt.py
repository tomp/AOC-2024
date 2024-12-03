#!/usr/bin/env python3
#
#  Advent of Code 2024 - Day 2
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
        7 6 4 2 1
        1 2 7 8 9
        9 7 6 2 1
        1 3 2 4 5
        8 6 4 4 1
        1 3 6 7 9
        """,
        2
    ),
]

SAMPLE_CASES2 = [
    (
        """
        7 6 4 2 1
        1 2 7 8 9
        9 7 6 2 1
        1 3 2 4 5
        8 6 4 4 1
        1 3 6 7 9
        """,
        4
    ),
    (
        """
        10 6 4 2 1
        5 8 4 2 1
        9 8 6 4 0
        1 0 3 4 5
        1 3 0 4 5
        1 3 4 0 5
        8 6 4 0 1
        """,
        7
    ),
    (
        """
        13 8 6 4 0
        0 9 6 2 1
        9 0 6 2 1
        """,
        0
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

def dampened_report_is_safe(levels: list[int]) -> bool:

    changes = [l2 - l1 for l1, l2 in zip(levels[:-1], levels[1:])]
    print(f"----\n {levels}  ^v {changes}")
    if all([delta in (1, 2, 3) for delta in changes]):
        print("<- SAFE")
        return True
    if all([delta in (-1, -2, -3) for delta in changes]):
        print("<- SAFE")
        return True

    for i in range(len(levels)):
        if i == 0 :
            report = levels[1:]
        elif i < len(levels)-1:
            report = levels[:i] + levels[i+1:]
        else:
            report = levels[:i]

        changes = [l2 - l1 for l1, l2 in zip(report[:-1], report[1:])]
        print(f"{i}: {report} ^v {changes}")
        if all([delta in (1, 2, 3) for delta in changes]):
            print("<- SAFE (dampened)")
            return True
        if all([delta in (-1, -2, -3) for delta in changes]):
            print("<- SAFE (dampened)")
            return True

    print("<- no safe dampening found")
    return False

def list_sign(changes: list[int]) -> int:
    count = defaultdict(int)
    for v in changes:
        count[sign(v)] += 1
        if count[sign(v)] > 2:
            return sign(v)
    return 0

def sign(x) -> int:
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def report_is_safe(levels: list[int]) -> bool:
    changes = [l2 - l1 for l1, l2 in zip(levels[:-1], levels[1:])]
    if all([delta in (1, 2, 3) for delta in changes]):
        return True
    if all([delta in (-1, -2, -3) for delta in changes]):
        return True
    return False

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    count = 0
    for line in lines:
        levels = list(map(int, line.strip().split()))
        if dampened_report_is_safe(levels):
            count += 1
    return count

def solve(lines: Lines) -> int:
    """Solve the problem."""
    count = 0
    for line in lines:
        levels = list(map(int, line.strip().split()))
        if report_is_safe(levels):
            count += 1
    return count


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
    assert result == 379
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
    assert result == 430
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
