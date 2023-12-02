from typing import Iterator

FILENAME = "test.txt"
COLORS = ["red", "green", "blue"]


def gen_rows(filename: str) -> Iterator:
    with open(filename, "r") as file:
        for line in file:
            yield line.rstrip()


def parse_rows(row: str):
    ...
