from collections import defaultdict
from time import perf_counter
from typing import Callable, Iterator

FILENAME = "input.txt"


def timer(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> str:
        start = perf_counter()
        res = func(*args, **kwargs)
        end = perf_counter()
        return f"Result = {res}. Execution took {(end-start) * 1000:.2f} ms."

    return wrapper


def gen_rows() -> Iterator[str]:
    with open(FILENAME, "r") as file:
        for line in file:
            yield line.rstrip()


def gen_winning_numbers_count() -> Iterator[tuple[int, int]]:
    for row in gen_rows():
        prefix, cards = row.split(": ")
        card_id = int(prefix.split()[1])
        winning, chosen = cards.split(" | ")
        winning_set = set(winning.split())
        chosen_set = set(chosen.split())
        yield card_id, len(winning_set.intersection(chosen_set))


def calculate_points(winning_count: int) -> int:
    return 2 ** (winning_count - 1) if winning_count else 0


def part1() -> int:
    total_points: int = sum(calculate_points(win_count) for _, win_count in gen_winning_numbers_count())
    return total_points


@timer
def part2_recursive() -> int:
    card_to_points: dict[int, int] = dict(gen_winning_numbers_count())
    scratch_count: int = len(card_to_points)

    def process_card(card_id: int) -> int:
        points = card_to_points[card_id]
        total_points_from_id = points
        ids_to_process = [card_id + i for i in range(1, points + 1)]
        for next_id in ids_to_process:
            total_points_from_id += process_card(next_id)
        return total_points_from_id

    for card_id in card_to_points:
        scratch_count += process_card(card_id)

    return scratch_count


@timer
def part2_dynamic() -> int:
    card_count: defaultdict = defaultdict(int)
    for card_id, win_count in gen_winning_numbers_count():
        card_count[card_id] += 1
        for i in range(win_count):
            card_count[card_id + 1 + i] += card_count[card_id]
    return sum(card_count.values())


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2 recursive: {part2_recursive()}")
    print(f"Part 2 dynamic: {part2_dynamic()}")
