from __future__ import annotations

from collections import deque
from enum import Enum
from time import perf_counter
from typing import Callable, Iterator, NamedTuple

FILENAME: str = "input.txt"
EMPTY, HSPLIT, VSPLIT, FSLANT, BSLANT = ".", "-", "|", "/", "\\"
SPLITTERS = [HSPLIT, VSPLIT]
MIRRORS = [FSLANT, BSLANT]


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


def parse_input() -> tuple[dict[tuple[int, int], str], tuple[int, int]]:
    res: dict[tuple[int, int], str] = {}
    r, c = 0, 0
    for r, line in enumerate(_gen_lines()):
        for c, char in enumerate(line):
            res[(r, c)] = char
    return res, (r + 1, c + 1)


class Coord(NamedTuple):
    r: int
    c: int

    def __add__(self, other: tuple) -> Coord:
        return Coord(r=self.r + other[0], c=self.c + other[1])


class Vector(NamedTuple):
    v: int
    h: int

    @property
    def opposite(self) -> Vector:
        return Vector(v=-self.v, h=-self.h)

    @property
    def turn(self) -> Vector:
        return Vector(v=self.h, h=self.v)


class Dir(Enum):
    N = Vector(-1, 0)
    E = Vector(0, 1)
    S = Vector(1, 0)
    W = Vector(0, -1)

    @classmethod
    def opposite(cls, vector: Vector) -> Dir:
        return cls(vector.opposite)

    @classmethod
    def turn(cls, vector: Vector) -> Dir:
        return cls(vector.turn)


class Beam:
    def __init__(self, coord: Coord, dir_: Dir):
        self.coord = coord
        self.dir = dir_

    def move(self) -> Coord:
        self.coord += self.dir.value
        return self.coord

    def process_field(self, field: str) -> Beam | None:
        if field == EMPTY:
            return None
        if field in SPLITTERS:
            return self._process_splitter(field)
        if field in MIRRORS:
            return self._process_mirror(field)  # type: ignore[func-returns-value]
        raise Exception(f"Unknown field: {field}")

    def _process_mirror(self, mirror: str) -> None:
        mapping: dict[str, dict[Dir, Dir]] = {
            FSLANT: {Dir.E: Dir.N, Dir.N: Dir.E, Dir.S: Dir.W, Dir.W: Dir.S},
            BSLANT: {Dir.E: Dir.S, Dir.S: Dir.E, Dir.N: Dir.W, Dir.W: Dir.N},
        }
        new_dir = mapping[mirror][self.dir]
        self.dir = new_dir
        return None

    def _process_splitter(self, splitter: str) -> Beam | None:
        if (self.dir in (Dir.N, Dir.S) and splitter == VSPLIT) or (self.dir in (Dir.E, Dir.W) and splitter == HSPLIT):
            return None
        turned: Dir = self.dir.turn(self.dir.value)
        turned_opposite: Dir = turned.opposite(turned.value)
        self.dir = turned
        return Beam(self.coord, turned_opposite)

    def __repr__(self):
        return f"{self.__class__.__name__} at {self.coord} moving in direction {self.dir}"


@timer
def part1() -> int:
    energized: set[Coord] = set()
    beams: deque[Beam] = deque([Beam(Coord(0, -1), Dir.E)])
    activated_splitters: set[Coord] = set()
    contraption, _ = parse_input()

    while beams:
        curr_beam = beams.pop()
        while True:
            loc = curr_beam.move()
            if loc not in contraption:
                break
            energized.add(loc)
            field = contraption[loc]
            if field == EMPTY:
                continue
            new_beam = curr_beam.process_field(field)
            if new_beam:
                if loc in activated_splitters:
                    break
                activated_splitters.add(loc)
                beams.append(new_beam)

    return len(energized)


def get_starting_locs(nr: int, nc: int) -> dict[Coord, Dir]:
    res: dict[Coord, Dir] = {}
    for r in range(nr):
        res[Coord(r, -1)] = Dir.E
        res[Coord(r, nc)] = Dir.W
    for c in range(nc):
        res[Coord(-1, c)] = Dir.S
        res[Coord(nr, c)] = Dir.N
    return res


@timer
def part2() -> int:
    contraption, size = parse_input()
    starting_points = get_starting_locs(size[0], size[1])

    max_energized = 0

    for start, direction in starting_points.items():
        energized: set[Coord] = set()
        beams: deque[Beam] = deque([Beam(start, direction)])
        activated_splitters: set[Coord] = set()

        while beams:
            curr_beam = beams.pop()
            while True:
                loc = curr_beam.move()
                if loc not in contraption:
                    break
                energized.add(loc)
                field = contraption[loc]
                if field == EMPTY:
                    continue
                new_beam = curr_beam.process_field(field)
                if new_beam:
                    if loc in activated_splitters:
                        break
                    activated_splitters.add(loc)
                    beams.append(new_beam)

        max_energized = max(max_energized, len(energized))

    return max_energized


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
