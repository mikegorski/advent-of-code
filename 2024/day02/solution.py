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


def check_safety(changes: list[int]) -> bool:
    valid_neg = {-1, -2, -3}
    valid_pos = {1, 2, 3}
    return all(n in valid_pos for n in changes) or all(n in valid_neg for n in changes)


@timer
def part1() -> int:
    safe_count: int = 0
    for line in _gen_lines():
        levels = [int(n) for n in line.split()]
        changes = [levels[i + 1] - n for i, n in enumerate(levels[:-1])]
        if check_safety(changes):
            safe_count += 1
    return safe_count


def check_dampened_safety(levels: list[int]) -> bool:
    for i in range(len(levels)):
        mod = levels[:i] + levels[i + 1 :]
        changes = [mod[i + 1] - n for i, n in enumerate(mod[:-1])]
        if check_safety(changes):
            return True
    return False


@timer
def part2() -> int:
    safe_count: int = 0
    for line in _gen_lines():
        levels = [int(n) for n in line.split()]
        changes = [levels[i + 1] - n for i, n in enumerate(levels[:-1])]
        if check_safety(changes):
            safe_count += 1
        elif check_dampened_safety(levels):
            safe_count += 1
    return safe_count


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
