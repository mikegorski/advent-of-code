from collections import defaultdict, deque
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


class Brick:
    def __init__(self, start: list[int], end: list[int]):
        self.cubes: list[list[int]] = self._get_cubes(start, end)
        self.supports: set[Brick] = set()
        self.supported_by: set[Brick] = set()
        self.vertical: bool = False

    def __iter__(self):
        return iter(self.cubes)

    def __getitem__(self, item):
        if item == -1:
            item = len(self.cubes) - 1
        if item < 0 or item >= len(self.cubes):
            raise IndexError
        return self.cubes[item]

    def fall(self, by: int) -> None:
        for i, cube in enumerate(self):
            self[i][-1] -= by

    def _get_cubes(self, start: list[int], end: list[int]) -> list[list[int]]:
        assert start <= end
        if start == end:
            return [start, end]
        cubes = [start]
        diff = [e - s for s, e in zip(start, end)]
        dr = next(i for i, v in enumerate(diff) if v)
        if dr == 2:
            self.vertical = True
        for _ in range(sum(diff)):
            cube = cubes[-1][:]
            cube[dr] += 1
            cubes.append(cube)
        assert cubes[-1] == end
        return cubes

    def simple_repr(self):
        return f"{self.__class__.__name__} {self.cubes[0]} ~ {self.cubes[-1]}"

    def __repr__(self):
        return (
            f"{self.simple_repr()} || Supports: {', '.join([s.simple_repr() for s in self.supports])}"
            f" || Supported by: {', '.join([s.simple_repr() for s in self.supported_by])}"
        )


def _gen_lines() -> Iterator[str]:
    with open(FILENAME, "r") as file:
        for line in file:
            yield line.rstrip()


def parse_input() -> list[Brick]:
    bricks: list[Brick] = []
    for line in _gen_lines():
        s, e = line.split("~")
        start = [int(d) for d in s.split(",")]
        end = [int(d) for d in e.split(",")]
        bricks.append(Brick(start, end))
    return bricks


def get_shift_and_supports(
    brick: Brick, lvl_map: dict[tuple[int, ...], int], cube_to_brick: dict[tuple[int, ...], Brick | None]
) -> tuple[int, list[Brick]]:
    highest_below_brick: dict[int, list[Brick]] = defaultdict(list)
    for cube in brick:
        h = lvl_map[tuple(cube[:-1])]
        if sup := cube_to_brick[(cube[0], cube[1], h)]:
            highest_below_brick[h].append(sup)
    max_h: int = max(highest_below_brick) if highest_below_brick else 0
    z_shift = brick[0][-1] - max_h - 1
    if not max_h:
        supports = []
    else:
        supports = list(set(highest_below_brick[max_h]))
    return z_shift, supports


@timer
def part1() -> int:
    bricks = parse_input()
    bricks.sort(key=lambda b: b[0][-1])
    lvl_map: dict[tuple[int, ...], int] = defaultdict(int)
    cube_to_brick: dict[tuple[int, ...], Brick | None] = defaultdict(lambda: None)
    for brick in bricks:
        z_shift, supports = get_shift_and_supports(brick, lvl_map, cube_to_brick)
        brick.fall(by=z_shift)
        if supports:
            for sup_brick in supports:
                brick.supported_by.add(sup_brick)
                sup_brick.supports.add(brick)
        for cube in brick:
            xy, z = cube[:-1], cube[-1]
            lvl_map[tuple(xy)] = z
            cube_to_brick[tuple(cube)] = brick

    cnt: int = 0
    for brick in bricks:
        if not len(brick.supports):
            cnt += 1
        else:
            if all(len(supported.supported_by) > 1 for supported in brick.supports):
                cnt += 1

    return cnt


@timer
def part2() -> int:
    bricks = parse_input()
    bricks.sort(key=lambda b: b[0][-1])
    lvl_map: dict[tuple[int, ...], int] = defaultdict(int)
    cube_to_brick: dict[tuple[int, ...], Brick | None] = defaultdict(lambda: None)
    for brick in bricks:
        z_shift, supports = get_shift_and_supports(brick, lvl_map, cube_to_brick)
        brick.fall(by=z_shift)
        if supports:
            for sup_brick in supports:
                brick.supported_by.add(sup_brick)
                sup_brick.supports.add(brick)
        for cube in brick:
            xy, z = cube[:-1], cube[-1]
            lvl_map[tuple(xy)] = z
            cube_to_brick[tuple(cube)] = brick

    safe_bricks: set[Brick] = set()
    for brick in bricks:
        if not len(brick.supports):
            safe_bricks.add(brick)
        else:
            if all(len(supported.supported_by) > 1 for supported in brick.supports):
                safe_bricks.add(brick)

    bricks.sort(key=lambda b: b[-1][-1], reverse=True)

    memo: dict[Brick, int] = {brick: 0 for brick in safe_bricks}

    for brick in bricks:
        if brick in memo:
            continue
        cnt: int = 0
        removed = {brick}
        queue = deque(brick.supports)
        while queue:
            curr = queue.popleft()
            if len(curr.supported_by.difference(removed)):
                continue
            cnt += 1
            removed.add(curr)
            for sup in curr.supports:
                if sup not in queue:
                    queue.append(sup)
        memo[brick] = cnt

    return sum(memo.values())


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
