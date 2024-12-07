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


def parse_input() -> tuple[list, list]:
    left, right = [], []
    for line in _gen_lines():
        ll, *_, rr = line.split(" ")
        left.append(ll)
        right.append(rr)
    return left, right


@timer
def part1() -> int:
    left, right = parse_input()
    left.sort()
    right.sort()
    return sum(abs(int(ll) - int(rr)) for ll, rr in zip(left, right))


@timer
def part2() -> int:
    left, right = parse_input()
    return sum(int(n) * right.count(n) for n in left)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
