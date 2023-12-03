import re
from collections import defaultdict
from math import prod
from typing import Iterator

FILENAME = "input.txt"
DIGITS = "0123456789"


def gen_rows() -> Iterator[str]:
    with open(FILENAME, "r") as file:
        for line in file:
            yield line.rstrip()


def gen_nums_locs() -> Iterator[tuple[int, list[tuple[int, int]]]]:
    for nrow, row in enumerate(gen_rows()):
        matches = re.finditer(r"\d+", row)
        for m in matches:
            num = int(m.group(0))
            locs = [(nrow, ncol) for ncol in range(m.start(), m.end())]
            yield num, locs


def get_adjacent_locs(nrow: int, ncol: int) -> list[tuple[int, int]]:
    locs = []
    for i in range(nrow - 1, nrow + 2):
        for j in range(ncol - 1, ncol + 2):
            locs.append((i, j))
    locs.remove((nrow, ncol))
    return locs


def get_all_adjacent_locs() -> set[tuple[int, int]]:
    adjacent: set[tuple[int, int]] = set()
    nonsymbols = set(f"{DIGITS}.")
    for nrow, row in enumerate(gen_rows()):
        for ncol, char in enumerate(row):
            if char not in nonsymbols:
                adjacent = adjacent | set(get_adjacent_locs(nrow, ncol))
    return adjacent


def part1() -> int:
    symbol_adjacent = get_all_adjacent_locs()
    return sum(num for num, locs in gen_nums_locs() if any((loc in symbol_adjacent for loc in locs)))


def get_all_star_adjacent_locs() -> dict[tuple[int, int], tuple[int, int]]:
    star_adjacent = {}
    for nrow, row in enumerate(gen_rows()):
        for ncol, char in enumerate(row):
            if char == "*":
                for loc in get_adjacent_locs(nrow, ncol):
                    star_adjacent[loc] = (nrow, ncol)
    return star_adjacent


def part2() -> int:
    star_adjacent = get_all_star_adjacent_locs()
    star_loc_to_numbers = defaultdict(list)

    for num, locs in gen_nums_locs():
        for loc in locs:
            if loc in star_adjacent:
                star_loc_to_numbers[star_adjacent[loc]].append(num)
                break

    return sum(prod(nums) for nums in star_loc_to_numbers.values() if len(nums) == 2)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
