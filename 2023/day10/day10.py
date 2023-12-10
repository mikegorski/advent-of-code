from __future__ import annotations

from time import perf_counter
from typing import Callable, Iterator, NamedTuple

import numpy as np
from matplotlib.path import Path


def timer(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> str:
        start = perf_counter()
        res = func(*args, **kwargs)
        end = perf_counter()
        return f"Result = {res}. Execution took {(end-start) * 1000:.2f} ms."

    return wrapper


class Dir(NamedTuple):
    x: int
    y: int

    def opposite(self) -> Dir:
        return Dir(x=-self.x, y=-self.y)


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: tuple):
        return Coord(self.x + other[0], self.y + other[1])


class Tile:
    def __init__(self, symbol: str, coord: Coord, prev: Tile | None = None):
        self.symbol = symbol
        self.coord = coord
        self.prev = prev
        self.next: Tile | None = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tile):
            return NotImplemented
        return self.symbol == other.symbol and self.coord == other.coord

    def get_next(self) -> Tile:
        if self.symbol == "S":
            return self._get_prev_and_next()
        for _dir in CONNS[self.symbol]:
            next_loc = self.coord + _dir
            if self.prev.coord == next_loc:  # type: ignore[union-attr]
                continue
            self.next = Tile(symbol=self.get_symbol_by_coord(next_loc), coord=next_loc, prev=self)
        assert self.next
        return self.next

    def _get_prev_and_next(self) -> Tile:
        connected: list[Tile] = []
        for _dir in CONNS[self.symbol]:
            next_loc = self.coord + _dir
            next_symbol = self.get_symbol_by_coord(next_loc)
            if _dir.opposite() in CONNS[next_symbol]:
                connected.append(Tile(symbol=next_symbol, coord=next_loc, prev=self))
        assert len(connected) == 2
        self.prev = connected[0]
        self.next = connected[1]
        return self.next

    @staticmethod
    def get_symbol_by_coord(coord: Coord) -> str:
        return AREA[coord.x][coord.y]

    def __repr__(self):
        return f"Symbol: {self.symbol}, coords: {self.coord}"


FILENAME: str = "input.txt"
AREA: list[list[str]] = []
CONNS: dict[str, list[Dir]] = {
    "F": [Dir(0, 1), Dir(1, 0)],
    "-": [Dir(0, -1), Dir(0, 1)],
    "7": [Dir(0, -1), Dir(1, 0)],
    "|": [Dir(1, 0), Dir(-1, 0)],
    "J": [Dir(0, -1), Dir(-1, 0)],
    "L": [Dir(0, 1), Dir(-1, 0)],
    "S": [Dir(0, 1), Dir(1, 0), Dir(0, -1), Dir(-1, 0)],
    ".": [],
}


def _gen_lines() -> Iterator[str]:
    with open(FILENAME, "r") as file:
        for line in file:
            yield line.rstrip()


def parse_map() -> tuple[int, int]:
    global AREA
    AREA = []
    start = None
    for n_row, line in enumerate(_gen_lines()):
        row = list(line)
        if not start:
            start = (n_row, row.index("S")) if "S" in row else None
        AREA.append(row)
    assert start
    return start


def get_loop(start_tile: Tile) -> list[Tile]:
    loop: list[Tile] = [start_tile]
    curr_tile = start_tile.get_next()
    loop.append(curr_tile)
    while curr_tile != start_tile.prev:
        curr_tile = curr_tile.get_next()
        loop.append(curr_tile)
    return loop


@timer
def part1() -> float:
    start_pos = parse_map()
    start_tile = Tile(symbol="S", coord=Coord(start_pos[0], start_pos[1]))
    loop = get_loop(start_tile)
    return len(loop) // 2


def calculate_tiles_inside_polygon(vertices: list[tuple[int, int]]) -> int:
    points: list[tuple[int, int]] = [
        (x, y) for x in range(len(AREA)) for y in range(len(AREA[0])) if (x, y) not in vertices
    ]
    p = Path(np.array(vertices))
    grid = p.contains_points(np.array(points))
    return np.count_nonzero(grid)


@timer
def part2() -> int:
    start_pos = parse_map()
    start_tile = Tile(symbol="S", coord=Coord(start_pos[0], start_pos[1]))
    loop = get_loop(start_tile)
    vertices = [(tile.coord.x, tile.coord.y) for tile in loop]
    return calculate_tiles_inside_polygon(vertices)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
