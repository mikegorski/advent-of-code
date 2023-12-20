from time import perf_counter
from typing import Callable, Iterator

FILENAME: str = "input.txt"
DIRS: dict[str, tuple[int, int]] = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


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


def parse_input() -> Iterator[tuple[str, int, str]]:
    for line in _gen_lines():
        dr, steps, color = line.split()
        yield dr, int(steps), color


def get_border(part: int = 1) -> tuple[list[tuple[int, int]], int]:
    border: list[tuple[int, int]] = [(0, 0)]
    l_border: int = 0
    for dr, steps, hex_s in parse_input():
        if part == 2:
            dr, steps = decode_hex(hex_s[2:-1])
        _dir = DIRS[dr]
        prev = border[-1]
        pos = prev[0] + _dir[0] * steps, prev[1] + _dir[1] * steps
        border.append(pos)
        l_border += steps

    return border[:-1], l_border


def decode_hex(s: str) -> tuple[str, int]:
    dr_map = {0: "R", 1: "D", 2: "L", 3: "U"}
    dst = int(s[:-1], 16)
    dr = int(s[-1])
    return dr_map[dr], dst


def inside_area(border: list[tuple[int, int]]) -> int:
    area = 0
    for i, p in enumerate(border[1:]):
        area += border[i + 1][0] * border[i][1] - border[i + 1][1] * border[i][0]
    return abs(area // 2)


@timer
def part1() -> int:
    border, l_border = get_border()
    return inside_area(border) + l_border // 2 + 1


@timer
def part2() -> int:
    border, l_border = get_border(part=2)
    return inside_area(border) + l_border // 2 + 1


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
