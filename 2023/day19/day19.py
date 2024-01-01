from collections import deque
from dataclasses import dataclass
from operator import gt, lt
from time import perf_counter
from typing import Callable, Iterator, Self

FILENAME: str = "input.txt"
OPERS: dict[str, Callable] = {"<": lt, ">": gt}


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


@dataclass
class Product:
    x: int
    m: int
    a: int
    s: int

    @property
    def total(self):
        return self.x + self.m + self.a + self.s


def _gen_lines() -> Iterator[str]:
    with open(FILENAME, "r") as file:
        for line in file:
            yield line.rstrip()


def parse_input() -> tuple[dict[str, list[str]], list[Product]]:
    input_gen = _gen_lines()
    workflows: dict[str, list[str]] = {}
    for line in input_gen:
        if line == "":
            break
        splt = line[:-1].split("{")
        workflows[splt[0]] = splt[1].split(",")

    products: list[Product] = []
    for line in input_gen:
        attrs = line[1:-1].split(",")
        x, m, a, s = [int(s[2:]) for s in attrs]
        products.append(Product(x, m, a, s))

    return workflows, products


def process(prod: Product, rule: str) -> str | None:
    if ":" not in rule:
        return rule
    comp, wf = rule.split(":")
    attr, op, val = comp[0], comp[1], int(comp[2:])
    if OPERS[op](getattr(prod, attr), val):
        return wf
    return None


@timer
def part1() -> int:
    workflows, products = parse_input()
    status: dict[str, list[Product]] = {"A": [], "R": []}

    for product in products:
        wf = "in"
        while wf not in "AR":
            for rule in workflows[wf]:
                nxt_wf = process(product, rule)
                if nxt_wf:
                    wf = nxt_wf
                    break

        status[wf].append(product)

    return sum(prod.total for prod in status["A"])


def reverse_map(target: str, workflows: dict[str, list[str]]) -> dict[str, str]:
    rule_to_wf: dict[str, str] = {}
    for wf, rules in workflows.items():
        for rule in rules:
            if rule == target or rule.endswith(f":{target}"):
                rule_to_wf[rule] = wf
    return rule_to_wf


class RangePart:
    def __init__(self, wf: str = "in", x=range(1, 4001), m=range(1, 4001), a=range(1, 4001), s=range(1, 4001)):
        self.wf = wf
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    @property
    def combinations(self):
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)

    def get_mod_copy_wf_only(self, wf: str) -> Self:
        new_inst: Self = self.__class__(**self.__dict__)
        setattr(new_inst, "wf", wf)
        return new_inst

    def get_mod_copy(self, rule: str, inverted: bool) -> Self:
        new_inst: Self = self.__class__(**self.__dict__)
        param, val, wf = self._get_param_and_val(rule, inverted)
        if not inverted:
            setattr(new_inst, "wf", wf)
            val = val + 1 if param.endswith("min") else val - 1
        param_r = getattr(new_inst, param[0])
        if param.endswith("min") and val > param_r.start:
            setattr(new_inst, param[0], range(val, param_r.stop))
        elif param.endswith("max") and val < param_r.stop - 1:
            setattr(new_inst, param[0], range(param_r.start, val + 1))
        return new_inst

    @staticmethod
    def _get_param_and_val(rule: str, inverted: bool) -> tuple[str, int, str]:
        m = {"<": "min", ">": "max"} if inverted else {">": "min", "<": "max"}
        comp, wf = rule.split(":")
        attr, op, val = comp[0], comp[1], int(comp[2:])
        param = attr + m[op]
        return param, val, wf

    def __repr__(self):
        return ", ".join([f"{k}={v}" for k, v in self.__dict__.items()]) + f" Total = {self.combinations}"


@timer
def part2() -> int:
    workflows, _ = parse_input()
    total: int = 0
    queue: deque[RangePart] = deque([RangePart()])

    while queue:
        curr_part: RangePart = queue.pop()
        if not curr_part.combinations:
            continue
        if curr_part.wf == "A":
            total += curr_part.combinations
        elif curr_part.wf == "R":
            continue
        else:
            rules = workflows[curr_part.wf]
            for rule in rules:
                if ":" in rule:
                    queue.append(curr_part.get_mod_copy(rule, inverted=False))
                    curr_part = curr_part.get_mod_copy(rule, inverted=True)
                else:
                    queue.append(curr_part.get_mod_copy_wf_only(wf=rule))
                    break
    return total


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
