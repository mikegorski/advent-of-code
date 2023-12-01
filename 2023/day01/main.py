FILE = "input.txt"
DIGITS = "0123456789"
SPELLED = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
VALID = list(DIGITS) + SPELLED


def part1():
    total = 0
    with open(FILE, "r") as file:
        for row in file:
            chars = row.rstrip()
            first_digit = next((char for char in chars if char in DIGITS), None)
            last_digit = next((char for char in chars[::-1] if char in DIGITS), None)
            total += int(first_digit + last_digit)
    return total


def part2():
    total = 0
    with open(FILE, "r") as file:
        for row in file:
            chars = row.rstrip()
            ind_left = {chars.find(d): d for d in VALID if chars.find(d) != -1}
            ind_right = {chars.rfind(d): d for d in VALID if chars.rfind(d) != -1}
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
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
