import re

FILENAME: str = "input.txt"


def parse_input() -> tuple[list[int], list[int]]:
    with open(FILENAME, "r") as file:
        lines = file.readlines()
    times = [int(t) for t in re.findall(r"\d+", lines[0])]
    dists = [int(d) for d in re.findall(r"\d+", lines[1])]
    return times, dists


def solve_quadratic_equation(a: int, b: int, c: int) -> tuple[float, float]:
    delta = b**2 - 4 * a * c
    if delta < 0:
        raise ValueError(f"{delta = }. No real roots exist.")
    r1 = -(b + delta**0.5) / (2 * a)
    r2 = (-b + delta**0.5) / (2 * a)
    return r1, r2


def count_ways(t_total: int, dist: int) -> int:
    r1, r2 = solve_quadratic_equation(a=-1, b=t_total, c=-dist)
    t_min, t_max = min(r1, r2), max(r1, r2)
    r_start = int(t_min) + 1
    r_end = int(t_max) - 1 if int(t_max) == t_max else int(t_max)
    return r_end - r_start + 1


def part1() -> int:
    times, dists = parse_input()
    ways_prod = 1
    for t_total, dist in zip(times, dists):
        ways_prod *= count_ways(t_total, dist)
    return ways_prod


def part2() -> int:
    times, dists = parse_input()
    time = int("".join([str(t) for t in times]))
    dist = int("".join([str(d) for d in dists]))
    return count_ways(time, dist)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
