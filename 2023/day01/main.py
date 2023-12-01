from typing import Iterator


FILENAME = "input.txt"
DIGITS = "0123456789"
SPELLED = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
VALID = list(DIGITS) + SPELLED


def gen_rows(filename: str) -> Iterator:
    with open(filename, "r") as file:
        for line in file:
            yield line.rstrip()


def part1(filename: str) -> int:
    total = 0
    for row in gen_rows(filename):
        first_digit = next((char for char in row if char in DIGITS), None)
        last_digit = next((char for char in row[::-1] if char in DIGITS), None)
        total += int(first_digit + last_digit)
    return total


def part2(filename: str) -> int:
    total = 0
    for row in gen_rows(filename):
        ind_left = {row.find(d): d for d in VALID if row.find(d) != -1}
        ind_right = {row.rfind(d): d for d in VALID if row.rfind(d) != -1}
        indices = ind_left | ind_right
        first_digit = indices[min(indices.keys())]
        last_digit = indices[max(indices.keys())]
        if first_digit in SPELLED:
            first_digit = SPELLED.index(first_digit) + 1
        if last_digit in SPELLED:
            last_digit = SPELLED.index(last_digit) + 1
        total += int(first_digit) * 10 + int(last_digit)
    return total


if __name__ == '__main__':
    print(f"Part 1: {part1(FILENAME)}")
    print(f"Part 2: {part2(FILENAME)}")
