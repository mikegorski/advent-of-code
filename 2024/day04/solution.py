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


def parse_input() -> list[str]:
    data: list[str] = list(_gen_lines())
    return data


def transpose(data: list[str]) -> list[str]:
    res: list[str] = ["".join(line[i] for line in data) for i in range(len(data[0]))]
    return res


def transpose_diagonally(data: list[str], reversed: bool = False) -> list[str]:
    diagonals: dict[int, list[str]] = {}
    for i, row in enumerate(data):
        for j, char in enumerate(row):
            diag_index = j - i if reversed else i + j
            if diag_index not in diagonals:
                diagonals[diag_index] = []
            diagonals[diag_index].append(char)

    return ["".join(diagonals[i]) for i in sorted(diagonals.keys())]


def count_occurences(data: list[str], word: str) -> int:
    total: int = 0
    for line in data:
        total += line.count(word) + line.count(word[::-1])
    return total


@timer
def part1() -> int:
    data_regular = parse_input()
    data_transposed = transpose(data_regular)
    data_diag_left_to_right = transpose_diagonally(data_regular)
    data_diag_right_to_left = transpose_diagonally(data_regular, reversed=True)

    word = "XMAS"
    total: int = 0
    for table in [data_regular, data_transposed, data_diag_left_to_right, data_diag_right_to_left]:
        total += count_occurences(table, word)
    return total


@timer
def part2() -> int:
    table = parse_input()
    proper_combinations = {"MSMS", "SSMM", "SMSM", "MMSS"}
    count: int = 0
    for c in range(1, len(table[0]) - 1):
        for r in range(1, len(table) - 1):
            combination = table[r - 1][c - 1] + table[r - 1][c + 1] + table[r + 1][c - 1] + table[r + 1][c + 1]
            if combination in proper_combinations and table[r][c] == "A":
                count += 1

    return count


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
