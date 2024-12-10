#!/usr/bin/env python3
#
#  Advent of Code 2024 - Day 9
#
from typing import Sequence, Generator, Union, Optional, Any, Dict, List, Tuple
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
        2333133121414131402
        """,
        1928
    ),
]

SAMPLE_CASES2 = [
    (
        """
        2333133121414131402
        """,
        2858
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

@dataclass
class Segment():
    pos: int
    size: int

    def __str__(self) -> str:
        return f"{self.pos}-{self.pos + self.size-1}"


class Diskmap():
    """A Diskmap represents how the blocks on a disk storage unit are being used."""

    def __init__(self, text: str):
        self.file = defaultdict(list)
        self.empty = []

        assert len(text) % 2 == 1, "Compressed disk map must have odd number of values"

        pos = 0
        for i in range(len(text) // 2):
            blocks = int(text[2*i])
            empty = int(text[2*i+1])
            self.file[i].append(Segment(pos, blocks))
            pos += blocks
            if empty:
                self.empty.append(Segment(pos, empty))
                pos += empty
        blocks = int(text[-1])
        self.file[i+1] = [Segment(pos, blocks)]
        self.empty.reverse()


    def __str__(self) -> str:
        lines = []
        lines.append("Files:")
        for fileno, segs in self.file.items():
            lines.append(f"  file {fileno}: {', '.join([str(seg) for seg in segs])}")
        lines.append("Empty blocks:")
        lines.append(', '.join([str(seg) for seg in reversed(self.empty)]))
        return "\n".join(lines)

    def allocate(self, need: int = 1, block_max: int = 0) -> list[Segment]:
        result = []
        while need > 0 and self.empty:
            if block_max and self.empty[-1].pos > block_max:
                break
            seg = self.empty.pop()
            if seg.size <= need:
                result.append(seg)
                need -= seg.size
            else:
                result.append(Segment(seg.pos, need))
                self.empty.append(Segment(seg.pos + need, seg.size - need))
                need = 0
        return result, need

    def allocate_one(self, need: int = 1, block_max: int = 0) -> Optional[Segment]:
        result = None
        if need > 0 and self.empty:
            for iseg in range(len(self.empty) - 1, -1, -1):
                seg = self.empty[iseg]
                if block_max and seg.pos > block_max:
                    return result, need
                if seg.size < need:
                    continue
                result = Segment(seg.pos, need)
                if seg.size == need:
                    self.empty = self.empty[:iseg] + self.empty[iseg+1:]
                else:
                    self.empty[iseg] = Segment(seg.pos + need, seg.size - need)
                need = 0
                return result, need
        return result, need

    def empty_blocks(self) -> int:
        return sum([seg.size for seg in self.empty])

    def checksum(self) -> int:
        result = 0
        for fileno, file_segs in self.file.items():
            for seg in file_segs:
                if seg.size == 1:
                    result += fileno * seg.pos
                else:
                    result += fileno * (seg.pos - 1) * seg.size
                    result += fileno * ((seg.size + 1) * seg.size // 2)
        return result


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    diskmap = Diskmap(lines[0].strip())

    # print("\nBefore...")
    # print(diskmap)

    for fileno, file_segs in sorted(diskmap.file.items(), reverse=True):
        assert len(file_segs) == 1
        file_seg = file_segs[0]
        seg, left = diskmap.allocate_one(file_seg.size, block_max=file_seg.pos)
        if left == 0:
            diskmap.file[fileno] = [seg]

    # print("\nAfter...")
    # print(diskmap)

    return diskmap.checksum()


def solve(lines: Lines) -> int:
    """Solve the problem."""
    diskmap = Diskmap(lines[0].strip())

    # print("\nBefore...")
    # print(diskmap)

    for fileno, file_segs in sorted(diskmap.file.items(), reverse=True):
        assert len(file_segs) == 1
        file_seg = file_segs[0]
        segs, left = diskmap.allocate(file_seg.size, block_max=file_seg.pos)
        # print(f"  file {fileno}: {file_seg} -> {', '.join([str(seg) for seg in segs])}")
        diskmap.file[fileno] = segs
        if left:
            diskmap.file[fileno].append(Segment(file_seg.pos, left))
            break

    # print("\nAfter...")
    # print(diskmap)

    return diskmap.checksum()


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
    assert result == 6330095022244
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
    assert result == 6359491814941
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
