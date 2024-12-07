import re
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


def parse_input() -> str:
    s: str = "".join(_gen_lines())
    return s


def find_instructions(data: str, pattern: str) -> Iterator[re.Match]:
    return re.finditer(pattern, data)


def multiply(instruction: str) -> int:
    start = instruction.find("(")
    end = instruction.find(")")
    nums = instruction[start + 1 : end]
    x, y = nums.split(",")
    return int(x) * int(y)


@timer
def part1() -> int:
    data = parse_input()
    mul_matches = find_instructions(data, pattern=r"mul\((\d{1,3}),(\d{1,3})\)")
    total: int = sum(multiply(m.group()) for m in mul_matches)
    return total


def get_instruction_starting_points(data: str, pattern: str) -> list[int]:
    matches = find_instructions(data, pattern)
    return [m.start() for m in matches]


def find_closest_lower(values, x):
    lower_values = [v for v in values if v < x]
    return max(lower_values) if lower_values else None


def is_enabled(dos: list[int], donts: list[int], pos: int) -> bool:
    do_closest = find_closest_lower(dos, pos)
    dont_closest = find_closest_lower(donts, pos)
    return do_closest > dont_closest if dont_closest else True


@timer
def part2() -> int:
    data = parse_input()
    mul_matches = find_instructions(data, pattern=r"mul\((\d{1,3}),(\d{1,3})\)")
    do_matches = find_instructions(data, pattern=r"do\(\)")
    dont_matches = find_instructions(data, pattern=r"don't\(\)")
    dos = [-1] + [m.start() for m in do_matches]
    donts = [m.start() for m in dont_matches]

    return sum(multiply(m.group()) for m in mul_matches if is_enabled(dos, donts, m.start()))


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
