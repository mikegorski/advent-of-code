import re
from math import prod
from typing import Iterator

FILENAME = "input.txt"


def gen_rows() -> Iterator[str]:
    with open(FILENAME, "r") as file:
        for line in file:
            yield line.rstrip()


def get_max_count(color: str, description: str) -> int:
    pattern = rf"\d+ {color}"
    if matches := re.findall(pattern, description):
        return max(map(lambda x: int(x.split()[0]), matches))
    else:
        return 0


def gen_parsed_rows() -> Iterator[tuple[int, tuple[int, int, int]]]:
    for row in gen_rows():
        game, round_desc = row.split(": ")
        game_id = int(game.split()[1])
        red_max_n = get_max_count("red", round_desc)
        green_max_n = get_max_count("green", round_desc)
        blue_max_n = get_max_count("blue", round_desc)
        yield game_id, (red_max_n, green_max_n, blue_max_n)


def game_possible(actual_rgb_counts: tuple[int, int, int], max_rgb_counts: tuple[int, int, int]) -> bool:
    return all(actual_cnt >= max_cnt for actual_cnt, max_cnt in zip(actual_rgb_counts, max_rgb_counts))


def part1(actual_rgb_counts: tuple[int, int, int]) -> int:
    total = 0
    for row in gen_parsed_rows():
        game_id, max_rgb_counts = row
        if game_possible(actual_rgb_counts, max_rgb_counts):
            total += game_id
    return total


def part2() -> int:
    total = 0
    for row in gen_parsed_rows():
        _, min_possible_rgb_count = row
        total += prod(min_possible_rgb_count)
    return total


if __name__ == "__main__":
    rgb_counts = (12, 13, 14)
    print(f"Part 1: {part1(rgb_counts)}")
    print(f"Part 2: {part2()}")
