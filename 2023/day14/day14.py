from collections import defaultdict
from time import perf_counter
from typing import Callable, Iterator

FILENAME: str = "input.txt"
DIRS: dict[str, tuple[int, int]] = {"N": (-1, 0), "W": (0, -1), "S": (1, 0), "E": (0, 1)}
N_CYCLES: int = 1_000_000_000


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


def _gen_rows() -> Iterator[str]:
    with open(FILENAME, "r") as file:
        for line in file:
            yield line.rstrip()


def parse_input() -> tuple[list[tuple[int, int]], set[tuple[int, int]], tuple[int, int]]:
    rounded: list[tuple[int, int]] = []
    cube: set[tuple[int, int]] = set()
    ir, ic = 0, 0
    for ir, row in enumerate(_gen_rows()):
        for ic, char in enumerate(row):
            if char == "O":
                rounded.append((ir, ic))
            elif char == "#":
                cube.add((ir, ic))
    return rounded, cube, (ir + 1, ic + 1)


def is_in_bounds(loc: tuple[int, int], size: tuple[int, int]) -> bool:
    return 0 <= loc[0] < size[0] and 0 <= loc[1] < size[1]


def sort_rounded(direction: str, rounded: list[tuple[int, int]]) -> list[tuple[int, int]]:
    dr = DIRS[direction]
    sort_index = next(i for i in range(2) if dr[i])
    mapping: dict[int, bool] = {-1: False, 1: True}
    rounded.sort(key=lambda x: x[sort_index], reverse=mapping[dr[sort_index]])
    return rounded


def tilt_platform(
    direction: str, rounded: list[tuple[int, int]], all_cube: set[tuple[int, int]], size: tuple[int, int]
) -> list[tuple[int, int]]:
    all_round: set[tuple[int, int]] = set(rounded)
    rock_to_shift: defaultdict[tuple[int, int], int] = defaultdict(int)
    rounded = sort_rounded(direction, rounded)
    dr = DIRS[direction]
    for i, rock in enumerate(rounded):
        nxt_pos: tuple[int, int] = rock[0] + dr[0], rock[1] + dr[1]
        while is_in_bounds(nxt_pos, size):
            if nxt_pos in all_round:
                rock_to_shift[rock] += rock_to_shift[nxt_pos]
                break
            if nxt_pos in all_cube:
                break
            rock_to_shift[rock] += 1
            nxt_pos = nxt_pos[0] + dr[0], nxt_pos[1] + dr[1]
        rounded[i] = rock[0] + dr[0] * rock_to_shift[rock], rock[1] + dr[1] * rock_to_shift[rock]
    return rounded


def run_cycle(
    rounded: list[tuple[int, int]], all_cube: set[tuple[int, int]], size: tuple[int, int]
) -> list[tuple[int, int]]:
    for direction in DIRS:
        rounded = tilt_platform(direction, rounded, all_cube, size)
    return rounded


@timer
def part1() -> int:
    rounded, all_cube, size = parse_input()
    rounded = tilt_platform("N", rounded, all_cube, size)
    return sum(size[0] - rock[0] for rock in rounded)


@timer
def part2() -> int:
    rounded, all_cube, size = parse_input()
    states_after_cycles: list[set[tuple[int, int]]] = []
    r_set: set[tuple[int, int]] = set()
    for _ in range(N_CYCLES):
        rounded = run_cycle(rounded, all_cube, size)
        r_set = set(rounded)
        if r_set in states_after_cycles:
            break
        states_after_cycles.append(r_set)

    cycle_start = states_after_cycles.index(r_set)
    cycle_len = len(states_after_cycles) - cycle_start
    last_cycles = (N_CYCLES - cycle_start) % cycle_len
    last_idx = cycle_start + last_cycles - 1 if last_cycles else cycle_start + cycle_len - 1

    return sum(size[0] - rock[0] for rock in list(states_after_cycles[last_idx]))


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
