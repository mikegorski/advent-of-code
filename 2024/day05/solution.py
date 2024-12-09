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


def parse_input() -> tuple[dict[int, set[int]], dict[int, set[int]], list[list[int]]]:
    gen = _gen_lines()
    after: dict[int, set[int]] = {}
    before: dict[int, set[int]] = {}
    for line in gen:
        if line == "":
            break
        a, b = [int(x) for x in line.split("|")]
        if a not in after:
            after[a] = set()
        if b not in before:
            before[b] = set()
        after[a].add(b)
        before[b].add(a)

    updates: list[list[int]] = [[int(x) for x in line.split(",")] for line in gen]

    return after, before, updates


def is_correct(update: list[int], after: dict[int, set[int]], before: dict[int, set[int]]) -> bool:
    for i, p in enumerate(update):
        pages_before = update[:i]
        pages_after = update[i + 1 :]

        if pages_before:
            if p not in before:
                return False
            if any((x not in before[p] for x in pages_before)):
                return False

        if pages_after:
            if p not in after:
                return False
            if any((x not in after[p] for x in pages_after)):
                return False

    return True


@timer
def part1() -> int:
    after, before, updates = parse_input()

    checksum: int = 0

    for update in updates:
        if is_correct(update, after, before):
            checksum += update[(len(update) - 1) // 2]

    return checksum


def get_correct_middle(update: list[int], after: dict[int, set[int]], before: dict[int, set[int]]) -> int:
    for i, p in enumerate(update):
        if p not in after or p not in before:
            continue
        other_pages = update[:i] + update[i + 1 :]
        pages_before_filtered = set(other_pages).intersection(before[p])
        pages_after_filtered = set(other_pages).intersection(after[p])
        if len(pages_after_filtered) == len(pages_before_filtered):
            return p
    return -10000000


@timer
def part2() -> int:
    after, before, updates = parse_input()

    checksum: int = 0

    for update in updates:
        if not is_correct(update, after, before):
            checksum += get_correct_middle(update, after, before)

    return checksum


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
