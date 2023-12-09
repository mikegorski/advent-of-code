from typing import Iterator

FILENAME = "input.txt"


def _gen_rows() -> Iterator[str]:
    with open(FILENAME, "r") as file:
        for line in file:
            yield line.rstrip()


def parse_rows() -> Iterator[list[int]]:
    for row in _gen_rows():
        yield [int(d) for d in row.split()]


def get_diffs(vals: list[int]) -> tuple[list[int], bool]:
    diffs = [vals[i] - vals[i - 1] for i in range(1, len(vals))]
    return diffs, len(set(diffs)) == 1


def forecast_fwd(vals: list[int]) -> int:
    all_zero: bool = False
    next_val = vals[-1]
    while not all_zero:
        vals, all_zero = get_diffs(vals)
        next_val += vals[-1]
    return next_val


def forecast_back(vals: list[int]) -> int:
    all_zero: bool = False
    next_val = [vals[0]]
    while not all_zero:
        vals, all_zero = get_diffs(vals)
        next_val.append(vals[0])
    return sum(-n if i % 2 else n for i, n in enumerate(next_val))


def part1() -> int:
    return sum(forecast_fwd(row) for row in parse_rows())


def part2() -> int:
    return sum(forecast_back(row) for row in parse_rows())


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
