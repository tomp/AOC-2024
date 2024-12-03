#!/usr/bin/env python3
#
#  Advent of Code 2024 - Day 3
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
        xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
        """,
        161
    ),
]

SAMPLE_CASES2 = [
    (
        """
        xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
        """,
        48
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

MUL_RE = re.compile(r"mul\((\d+),(\d+)\)")
INSTRUCTION_RE = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")

INST_MUL = "mul("
INST_DO = "do("
INST_DONT = "don't("

def find_enabled_muls(text: str) -> list[Tuple[int, int]]:
    result = []
    enabled = True
    for m in INSTRUCTION_RE.finditer(text):
        if m:
            inst = m.group(0)
            if inst.startswith(INST_MUL):
                if enabled:
                    m2 = MUL_RE.match(inst)
                    a, b = m2.groups()
                    # print(f"--> mul({a},{b})")
                    result.append((int(a), int(b)))
            elif inst.startswith(INST_DO):
                # print("--> ENABLED")
                enabled = True
            elif inst.startswith(INST_DONT):
                # print("--> DISABLED")
                enabled = False
            else:
                print(f"!!!! UNEXPECTED MATCH ON {inst}")
    return result

def find_muls(text: str) -> list[Tuple[int, int]]:
    result = []
    for m in MUL_RE.finditer(text):
        if m:
            a, b = m.groups()
            # print(f"--> mul({a},{b})")
            result.append((int(a), int(b)))
    return result

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    result = 0
    text = " ".join([line.strip() for line in lines])
    for a, b in find_enabled_muls(text):
        result += a * b
    return result

def solve(lines: Lines) -> int:
    """Solve the problem."""
    result = 0
    text = " ".join([line.strip() for line in lines])
    for a, b in find_muls(text):
        result += a * b
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
    assert result == 167090022
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
    assert result == 89823704
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
