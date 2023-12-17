from time import perf_counter
from typing import Callable, Iterator

FILENAME: str = "input.txt"


class ReflectionNotFound(Exception):
    def __init__(self, pattern):
        self.pattern = pattern

    def __str__(self):
        info_line = "No reflection found for the following pattern: \n"
        printed_pattern = "\n".join(self.pattern)
        return info_line + printed_pattern


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


def gen_patterns() -> Iterator[list[str]]:
    pattern: list[str] = []
    for line in _gen_lines():
        if not line:
            yield pattern
            pattern = []
        else:
            pattern.append(line)
    yield pattern


def find_horizontal(pattern: list[str]) -> tuple[int, int] | None:
    for i in range(len(pattern) - 1):
        n_pairs = min(i + 1, len(pattern) - i - 1)
        found = all(pattern[i - j] == pattern[i + 1 + j] for j in range(n_pairs))
        if found:
            return i, i + 1
    return None


def transpose(pattern: list[str]) -> list[str]:
    transposed: list[str] = ["".join(row[col] for row in reversed(pattern)) for col in range(len(pattern[0]))]
    return transposed


def find_vertical(pattern: list[str]) -> tuple[int, int] | None:
    pattern = transpose(pattern)
    return find_horizontal(pattern)


@timer
def part1() -> int:
    total = 0
    for pattern in gen_patterns():
        if hor := find_horizontal(pattern):
            total += hor[1] * 100
        elif vert := find_vertical(pattern):
            total += vert[1]
        else:
            raise ReflectionNotFound(pattern)
    return total


def almost_equal(s1: str, s2: str) -> bool:
    return [a != b for a, b in zip(s1, s2)].count(True) == 1


def find_horizontal_with_smudge(pattern: list[str]) -> tuple[int, int] | None:
    for i in range(len(pattern) - 1):
        n_pairs = min(i + 1, len(pattern) - i - 1)
        exact_matches = [pattern[i - j] == pattern[i + 1 + j] for j in range(n_pairs)]
        smudge_matches = [almost_equal(pattern[i - j], pattern[i + 1 + j]) for j in range(n_pairs)]
        found = exact_matches.count(True) == n_pairs - 1 and smudge_matches.count(True) == 1
        if found:
            return i, i + 1
    return None


def find_vertical_with_smudge(pattern: list[str]) -> tuple[int, int] | None:
    pattern = transpose(pattern)
    return find_horizontal_with_smudge(pattern)


@timer
def part2() -> int:
    total = 0
    for pattern in gen_patterns():
        if hor := find_horizontal_with_smudge(pattern):
            total += hor[1] * 100
        elif vert := find_vertical_with_smudge(pattern):
            total += vert[1]
        else:
            raise ReflectionNotFound(pattern)
    return total


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
