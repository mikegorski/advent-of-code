from typing import Iterator

FILENAME = "input.txt"
CARD_TO_VALUE_1: dict[str, int] = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}
TYPE_TO_VALUE: dict[str, int] = {"11111": 1, "1112": 2, "122": 3, "113": 4, "23": 5, "14": 6, "5": 7}
CARD_TO_VALUE_2: dict[str, int] = {
    "J": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def _gen_rows() -> Iterator[str]:
    with open(FILENAME, "r") as file:
        for line in file:
            yield line.rstrip()


def get_hand_to_bid_mapping() -> dict[str, int]:
    res: dict[str, int] = {}
    for row in _gen_rows():
        _list = row.split()
        res[_list[0]] = int(_list[1])
    return res


def _get_hand_type(hand: str) -> str:
    unique = list(set(hand))
    return "".join(sorted([str(hand.count(card)) for card in unique]))


def _get_cards_values(hand: str, mapping: dict[str, int]) -> int:
    return sum(mapping[card] * 10 ** (8 - 2 * i) for i, card in enumerate(hand))


def get_hand_value(hand: str) -> int:
    hand_type = _get_hand_type(hand)
    hand_value = TYPE_TO_VALUE[hand_type] * 1e10 + _get_cards_values(hand, CARD_TO_VALUE_1)
    return int(hand_value)


def part1() -> int:
    hand_to_bid = get_hand_to_bid_mapping()
    ordering: list[tuple[str, int]] = [(hand, get_hand_value(hand)) for hand in hand_to_bid]
    ordering.sort(key=lambda x: x[1])
    return sum(hand_to_bid[hand] * (i + 1) for i, (hand, _) in enumerate(ordering))


def _get_hand_type_with_jokers(hand: str) -> str:
    joker_count = hand.count("J")
    if not joker_count or joker_count == 5:
        return _get_hand_type(hand)
    type_without_joker = _get_hand_type("".join([c for c in hand if c != "J"]))
    last = type_without_joker[-1]
    return type_without_joker[:-1] + str(int(last) + joker_count)


def get_hand_value_with_jokers(hand: str) -> int:
    hand_type = _get_hand_type_with_jokers(hand)
    hand_value = TYPE_TO_VALUE[hand_type] * 1e10 + _get_cards_values(hand, CARD_TO_VALUE_2)
    return int(hand_value)


def part2() -> int:
    hand_to_bid = get_hand_to_bid_mapping()
    ordering: list[tuple[str, int]] = [(hand, get_hand_value_with_jokers(hand)) for hand in hand_to_bid]
    ordering.sort(key=lambda x: x[1])
    return sum(hand_to_bid[hand] * (i + 1) for i, (hand, _) in enumerate(ordering))


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
