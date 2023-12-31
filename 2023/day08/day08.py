import itertools
import math
import re
from typing import Iterator

FILENAME = "input.txt"


def _gen_rows() -> Iterator[str]:
    with open(FILENAME, "r") as file:
        for line in file:
            yield line.rstrip()


def parse_input() -> tuple[list[int], dict[str, tuple[str, str]]]:
    line_gen = _gen_rows()
    instructions = [int(d) for d in next(line_gen).replace("L", "0").replace("R", "1")]
    _ = next(line_gen)
    mapping: dict[str, tuple[str, str]] = {}
    for line in line_gen:
        matches = re.findall(r"\w+", line)
        mapping[matches[0]] = (matches[1], matches[2])
    return instructions, mapping


def navigate(start: str, end: str, instructions: list[int], mapping: dict[str, tuple[str, str]]) -> int:
    nxt = start
    steps = 0
    dir_iter = itertools.cycle(instructions)

    while not nxt.endswith(end):
        direction = next(dir_iter)
        nxt = mapping[nxt][direction]
        steps += 1
    return steps


def part1() -> int:
    instructions, mapping = parse_input()
    return navigate("AAA", "ZZZ", instructions, mapping)


def part2() -> int:
    instructions, mapping = parse_input()
    starting_points = [k for k in mapping if k.endswith("A")]
    return math.lcm(*[navigate(start, "Z", instructions, mapping) for start in starting_points])


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
