#!/usr/bin/env python3
#
#  Advent of Code 2024 - Day 5
#
from typing import Sequence, Union, Optional, Any, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint, pformat
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
        """,
        143
    ),
]

SAMPLE_CASES2 = [
    (
        """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
        """,
        123
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
        # print(f">> {line.strip()}")
        if not line.strip():
            if sect:
                result.append(sect)
                # print(f"section:\n{'\n'.join(sect)}")
            sect = []
        else:
            sect.append(line)
    if sect:
        result.append(sect)
        # print(f"section:\n{'\n'.join(sect)}")
    return result


# Solution

Rules = dict[int, set[int]]
Update = list[int]

def parse_input(lines) -> Tuple[Rules, list[Update]]:
    rules = defaultdict(set)
    updates = []

    sect1, sect2 = parse_sections(lines)

    for line in sect1:
        before, after = map(int, line.strip().split('|'))
        rules[before].add(after)

    for line in sect2:
        updates.append(list(map(int, line.strip().split(","))))

    return rules, updates

def update_is_correct(rules: Rules, update: Update) -> bool:
    for i in range(1, len(update)):
        after = update[i]
        if any([before in rules[after] for before in update[:i]]):
            return False
    return True

def correct_update(rules: Rules, update: Update) -> Tuple[Update, bool]:
    # print(f"----\ninitial: {update}")
    for i in range(1, len(update)):
        after = update[i]
        for j in range(i):
            before = update[j]
            if before in rules[after]:
                # print(f"!! page[{j}] {before} must follow page[{i}] {after}")
                new_update = update[:j] + update[i:i+1] + update[j:i] + update[i+1:]
                # print(f"reorder -> {new_update}")
                return new_update, False
    return update, True

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    result = 0
    rules, updates = parse_input(lines)
    # print("Rules:\n", pformat(rules), "\n")
    for update in updates:
        # print(f">> {update}")
        ok = update_is_correct(rules, update)
        if ok:
            continue
        while not ok:
            update, ok = correct_update(rules, update)
        middle = update[len(update)//2]
        # print(f"--> CORRECT (add {middle})")
        result += middle
    return result

def solve(lines: Lines) -> int:
    """Solve the problem."""
    result = 0
    rules, updates = parse_input(lines)
    # print("Rules:\n", pformat(rules), "\n")
    for update in updates:
        # print(f">> {update}")
        if update_is_correct(rules, update):
            middle = update[len(update)//2]
            # print(f"--> CORRECT (add {middle})")
            result += middle
        # else:
        #     print(f"--> not correct")

    return result


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text, blank_lines=True)
        result = solve(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 4957
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, expected in SAMPLE_CASES2:
        lines = load_text(text, blank_lines=True)
        result = solve2(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    assert result == 6938
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE, blank_lines=True)
    part1(input_lines)
    example2()
    part2(input_lines)
