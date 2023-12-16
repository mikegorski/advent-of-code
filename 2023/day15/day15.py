from time import perf_counter
from typing import Callable

FILENAME: str = "input.txt"


def timer(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> str:
        start = perf_counter()
        res = func(*args, **kwargs)
        end = perf_counter()
        return f"Result = {res}. Execution took {(end-start) * 1000:.2f} ms."

    return wrapper


def get_strings() -> list[str]:
    with open(FILENAME, "r") as file:
        line = file.readline()
    return line.split(",")


def hash_char(c: str, curr: int) -> int:
    curr += ord(c)
    curr *= 17
    curr %= 256
    return curr


def hash_str(s: str) -> int:
    val = 0
    for c in s:
        val = hash_char(c, val)
    return val


@timer
def part1() -> int:
    strings = get_strings()
    return sum(hash_str(s) for s in strings)


def split_str(s: str) -> tuple[str, int]:
    if s.endswith("-"):
        return s[:-1], 0
    label, focal = s.split("=")
    return label, int(focal)


@timer
def part2() -> int:
    strings = get_strings()
    boxes: list[tuple[list[str], list[int]]] = [([], []) for _ in range(256)]
    not_empty: set[int] = set()
    label_to_hash: dict[str, int] = {}

    for s in strings:
        label, focal = split_str(s)
        nbox = label_to_hash.setdefault(label, hash_str(label))
        if focal:
            if label in boxes[nbox][0]:
                i = boxes[nbox][0].index(label)
                boxes[nbox][1][i] = focal
            else:
                boxes[nbox][0].append(label)
                boxes[nbox][1].append(focal)
                not_empty.add(nbox)
            continue
        if label in boxes[nbox][0]:
            i = boxes[nbox][0].index(label)
            del boxes[nbox][0][i]
            del boxes[nbox][1][i]

    total = 0
    for i, box in enumerate(boxes):
        for j, focal in enumerate(box[1]):
            total += (i + 1) * (j + 1) * focal
    return total


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
