from functools import wraps
from time import perf_counter
from typing import Callable, Iterator

FILENAME: str = "input.txt"
MAP_NAME_EOL: str = ":"
NEXT_MAP: str = ""


def timer(f=None, n=10) -> Callable:
    def decorator(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs) -> str:
            total_time: float = 0
            res = 0
            for _ in range(n):
                start = perf_counter()
                res = fn(*args, **kwargs)
                end = perf_counter()
                total_time += end - start
            avg = total_time / n
            return f"Result = {res}. Execution took {avg * 1000:.2f} ms on average in {n} trials."

        return wrapper

    return decorator(f) if callable(f) else decorator


def gen_lines() -> Iterator[str]:
    with open(FILENAME, "r") as file:
        for line in file:
            yield line.rstrip()


def parse_numbers_line(line: str) -> tuple[int, range]:
    dest_start, src_start, n = [int(x) for x in line.split()]
    src_dest_offset = src_start - dest_start
    src_range = range(src_start, src_start + n)
    return src_dest_offset, src_range


def parse_input() -> tuple[list[int], dict[str, dict[range, int]]]:
    line_generator = gen_lines()

    seeds_line = next(line_generator)
    _ = next(line_generator)
    seeds: list[int] = [int(s) for s in seeds_line.split(": ")[1].split()]

    next_key: str = ""
    next_mapping: dict[range, int] = {}
    mappings: dict[str, dict[range, int]] = {}

    for line in line_generator:
        if line.endswith(MAP_NAME_EOL):
            next_key = line.split()[0]
            next_mapping = {}
        elif line == NEXT_MAP:
            mappings[next_key] = next_mapping
        else:
            offset, src_range = parse_numbers_line(line)
            next_mapping[src_range] = offset

    mappings[next_key] = next_mapping

    return seeds, mappings


def map_seed_to_loc(seed: int, mappings: dict[str, dict[range, int]]) -> int:
    for curr_map in mappings.values():
        for src_range, offset in curr_map.items():
            if seed in src_range:
                seed -= offset
                break
    return seed


@timer(n=100)
def part1():
    seeds, mappings = parse_input()
    lowest_loc = float("inf")
    for seed in seeds:
        loc = map_seed_to_loc(seed, mappings)
        lowest_loc = min(lowest_loc, loc)
    return lowest_loc


def convert_seed_list_to_ranges(seeds: list[int]) -> list[range]:
    start_nums: list[int] = seeds[::2]
    n_vals: list[int] = seeds[1::2]
    seed_ranges: list[range] = [range(start, start + n) for start, n in zip(start_nums, n_vals)]
    return seed_ranges


def get_endpoints_from_ranges(ranges: list[range]) -> list[int]:
    ranges = sorted(ranges, key=lambda r: r.start)
    result: list[int] = []
    for r in ranges:
        result.extend((r.start, r.stop - 1))
    return result


def reverse_map(initial: list[int], mapping: dict[range, int]) -> list[int]:
    result: list[int] = []
    checked: set[int] = set()

    for num in initial:
        for r, offset in mapping.items():
            if (num + offset) in r:
                result.append(num + offset)
                checked.add(num)
                break
        if num not in checked:
            result.append(num)

    ranges_endpoints = get_endpoints_from_ranges(list(mapping.keys()))
    result.extend(ranges_endpoints)
    result.extend((ranges_endpoints[0] - 1, ranges_endpoints[-1] + 1))
    return sorted(list(set(result)))


def get_trimmed_seed_list(seeds: list[int], seed_ranges: list[range]) -> list[int]:
    result = [s for s in seeds if any((s in r for r in seed_ranges))]
    result.extend(get_endpoints_from_ranges(seed_ranges))
    return sorted(list(set(result)))


@timer
def part2():
    seeds, mappings = parse_input()
    seed_ranges = convert_seed_list_to_ranges(seeds)
    to_check: list[int] = []

    for map_name in reversed(mappings.keys()):
        to_check = reverse_map(to_check, mappings[map_name])

    seeds_to_check = get_trimmed_seed_list(to_check, seed_ranges)

    lowest_loc = float("inf")
    for seed in seeds_to_check:
        loc = map_seed_to_loc(seed, mappings)
        lowest_loc = min(lowest_loc, loc)
    return lowest_loc


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
