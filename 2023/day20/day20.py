from abc import ABC, abstractmethod
from collections import defaultdict, deque
from math import lcm
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


class Module(ABC):
    def __init__(self, targets: list[str]):
        self.targets = targets

    @abstractmethod
    def process_input(self, pulse: int, src: str) -> None:
        pass

    @abstractmethod
    def output(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__} module | Targets: {', '.join(self.targets)}."


class Broadcaster(Module):
    def __init__(self, targets: list[str]):
        super().__init__(targets)
        self.pulse: int = 0

    def process_input(self, pulse: int = 0, src: str = ""):
        self.pulse = pulse

    def output(self) -> tuple[int, list[str]]:
        return self.pulse, self.targets


class FlipFlop(Module):
    def __init__(self, targets: list[str]):
        super().__init__(targets)
        self.state = 0
        self.pulse: int | None = None

    def process_input(self, pulse: int, src: str) -> None:
        if pulse:
            self.pulse = None
        else:
            self.state = 0 if self.state else 1
            self.pulse = self.state

    def output(self) -> tuple[int | None, list[str]]:
        return self.pulse, self.targets


class Conjunction(Module):
    def __init__(self, targets: list[str]):
        super().__init__(targets)
        self.inputs: dict[str, int] = {}

    def process_input(self, pulse: int, src: str):
        self.inputs[src] = pulse

    def output(self) -> tuple[int, list[str]]:
        pulse: int = 0 if all(v for v in self.inputs.values()) else 1
        return pulse, self.targets

    def __repr__(self):
        return (
            f"Conjunction module | "
            f"Inputs: {', '.join([f'{k}={v}' for k, v in self.inputs.items()])} | "
            f"Targets: {', '.join(self.targets)}."
        )


def _gen_lines() -> Iterator[str]:
    with open(FILENAME, "r") as file:
        for line in file:
            yield line.rstrip()


def parse_input() -> dict[str, Module]:
    res: dict[str, Module] = {}
    for line in _gen_lines():
        typename, targets = line.split(" -> ")
        if typename == "broadcaster":
            res[typename] = Broadcaster(targets=targets.split(", "))
            continue
        type_, name = typename[0], typename[1:]
        if type_ not in "%&":
            raise Exception("Unknown module type.")
        module_class = FlipFlop if type_ == "%" else Conjunction
        res[name] = module_class(targets=targets.split(", "))
    return res


def update_conjunction_modules(mapping: dict[str, Module]) -> dict[str, Module]:
    conj_modules: list[str] = []
    target_to_input: defaultdict = defaultdict(list)
    for name, module in mapping.items():
        if isinstance(module, Conjunction):
            conj_modules.append(name)
        for target in module.targets:
            target_to_input[target].append(name)
    for name in conj_modules:
        for inp in target_to_input[name]:
            mod = mapping[name]
            assert isinstance(mod, Conjunction)
            mod.inputs[inp] = 0
    return mapping


def serialize(mapping: dict[str, Module]) -> str:
    s: str = ""
    for name, mod in mapping.items():
        s += name + repr(mod)
    return s


@timer
def part1() -> int:
    modules = parse_input()
    modules = update_conjunction_modules(modules)

    pushes: int = 1000
    counter: dict[int, int] = {0: 0, 1: 0}

    for push in range(pushes):
        pulses: deque[tuple[str, int, str]] = deque([("button", 0, "broadcaster")])
        while pulses:
            src, pulse, target = pulses.popleft()
            if pulse is None:
                continue
            counter[pulse] += 1
            if target in modules:
                modules[target].process_input(pulse, src)
                new_src = target
                pulse, targets = modules[target].output()
                for target in targets:
                    pulses.append((new_src, pulse, target))

    return counter[0] * counter[1]


@timer
def part2() -> int:
    modules = parse_input()
    modules = update_conjunction_modules(modules)

    rx_mod: str = ""
    for name, mod in modules.items():
        if "rx" in mod.targets:
            rx_mod = name
            break

    rx_mod_sources: list[str] = []
    for name, mod in modules.items():
        if rx_mod in mod.targets:
            rx_mod_sources.append(name)

    rx_cycles: defaultdict = defaultdict(list)

    n = 1
    while len(rx_cycles) < len(rx_mod_sources):
        pulses: deque[tuple[str, int, str]] = deque([("button", 0, "broadcaster")])
        while pulses:
            src, pulse, target = pulses.popleft()
            if src in rx_mod_sources and pulse == 1:
                rx_cycles[src] = n
            if pulse is None:
                continue
            if target in modules:
                modules[target].process_input(pulse, src)
                new_src = target
                pulse, targets = modules[target].output()
                for target in targets:
                    pulses.append((new_src, pulse, target))
        n += 1

    return lcm(*rx_cycles.values())


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
