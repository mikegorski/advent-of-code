from time import perf_counter
from typing import Callable, Iterator, TypeAlias

FILENAME: str = "input.txt"
Numeric: TypeAlias = int | float


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


def parse_input() -> tuple[complex, tuple[int, int], set[complex]]:
    start = None
    rocks: set[complex] = set()
    ir, ic = 0, 0
    for ir, line in enumerate(_gen_lines()):
        if not start:
            if "S" in line:
                start = ir + line.index("S") * 1j
        for ic, char in enumerate(line):
            if char == "#":
                rocks.add(ir + ic * 1j)
    if not start:
        raise Exception("Starting position not found - check your input data.")
    return start, (ir + 1, ic + 1), rocks


@timer
def part1() -> int:
    start, size, rocks = parse_input()
    steps: int = 64 if FILENAME == "input.txt" else 6
    reached: set[complex] = {start}
    dirs: list[complex] = [1j, -1j, -1, 1]

    for i in range(steps):
        reached = {p + d for d in dirs for p in reached if p + d not in rocks}
    return len(reached)


def cmod(loc: complex, size: tuple[int, int]) -> complex:
    return loc.real % size[0] + loc.imag % size[1] * 1j


@timer
def part2() -> int:
    start, size, rocks = parse_input()
    total_steps: int = 26501365
    base: int = total_steps % size[0]
    cycle: int = size[0]
    reached: set[complex] = {start}
    dirs: list[complex] = [1j, -1j, -1, 1]
    y_vals: list[int] = []

    for i in range(base + 2 * cycle + 1):
        if i % cycle == base:
            y_vals.append(len(reached))
        reached = {p + d for d in dirs for p in reached if cmod(p + d, size) not in rocks}

    u0, u1, u2 = y_vals
    d0 = u0
    d1 = u1 - u0
    d2 = u2 - 2 * u1 + u0
    n = 26501365 // cycle
    return d2 * n * (n - 1) // 2 + d1 * n + d0


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
