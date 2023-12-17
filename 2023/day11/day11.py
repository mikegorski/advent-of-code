from itertools import combinations
from time import perf_counter
from typing import Callable, Iterator

FILENAME: str = "input.txt"


def timer(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> str:
        start = perf_counter()
        res = func(*args, **kwargs)
        end = perf_counter()
        total = end - start
        mult: int = 1000
        unit: str = "ms"
        if total >= 1:
            mult = 1
            unit = "s"
        return f"Result = {res}. Execution took {total * mult:.2f} {unit}."

    return wrapper


def _gen_lines() -> Iterator[str]:
    with open(FILENAME, "r") as file:
        for line in file:
            yield line.rstrip()


def get_space_data() -> tuple[list[tuple[int, int]], list[int], list[int]]:
    galaxies: list[tuple[int, int]] = []
    rows_with_galaxies: set[int] = set()
    cols_with_galaxies: set[int] = set()
    ir, ic = 0, 0
    for ir, line in enumerate(_gen_lines()):
        for ic, char in enumerate(line):
            if char == "#":
                galaxies.append((ir, ic))
                rows_with_galaxies.add(ir)
                cols_with_galaxies.add(ic)
    r_exp = set(list(range(ir))) - rows_with_galaxies
    c_exp = set(list(range(ic))) - cols_with_galaxies
    return galaxies, list(r_exp), list(c_exp)


def expand(galaxies: list[tuple[int, int]], r_exp: list[int], c_exp: list[int], rate: int) -> list[tuple[int, int]]:
    for i, galaxy in enumerate(galaxies):
        r_inc = sum(galaxy[0] > r_num for r_num in r_exp)
        c_inc = sum(galaxy[1] > c_num for c_num in c_exp)
        galaxies[i] = (galaxy[0] + r_inc * (rate - 1), galaxy[1] + c_inc * (rate - 1))

    return galaxies


def get_dist(start: tuple[int, int], end: tuple[int, int]) -> int:
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def get_sum_of_distances(galaxies: list[tuple[int, int]]) -> int:
    total: int = sum(get_dist(start, end) for start, end in combinations(galaxies, 2))
    return total


@timer
def part1() -> int:
    galaxies = expand(*get_space_data(), rate=2)
    return get_sum_of_distances(galaxies)


@timer
def part2() -> int:
    galaxies = expand(*get_space_data(), rate=1_000_000)
    return get_sum_of_distances(galaxies)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
