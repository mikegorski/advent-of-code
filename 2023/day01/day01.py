from typing import Iterator

FILENAME = "input.txt"
DIGITS = "0123456789"
SPELLED = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
VALID = list(DIGITS) + SPELLED


def gen_rows() -> Iterator:
    with open(FILENAME, "r") as file:
        for line in file:
            yield line.rstrip()


def part1() -> int:
    total = 0
    for row in gen_rows():
        first_digit = next(char for char in row if char in DIGITS)
        last_digit = next(char for char in row[::-1] if char in DIGITS)
        total += int(first_digit + last_digit)
    return total


def part2() -> int:
    total = 0
    for row in gen_rows():
        ind_left = {row.find(d): d for d in VALID if row.find(d) != -1}
        ind_right = {row.rfind(d): d for d in VALID if row.rfind(d) != -1}
        indices = ind_left | ind_right
        first_digit: str = indices[min(indices.keys())]
        last_digit: str = indices[max(indices.keys())]
        if first_digit in SPELLED:
            first_digit = str(SPELLED.index(first_digit) + 1)
        if last_digit in SPELLED:
            last_digit = str(SPELLED.index(last_digit) + 1)
        total += int(first_digit) * 10 + int(last_digit)
    return total


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
