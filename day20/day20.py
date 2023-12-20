import os
from queue import Queue

import graphviz
from lib.classes import BaseModule, Pulse, PulseTarget
from lib.parsers_20 import finalize_modules, get_modules

FILE_A = "input-a.txt"
FILE_B = "input-b.txt"
FILE_PROD = "input.txt"

FILE = FILE_PROD


def simulate(modules: dict[str, BaseModule]) -> tuple[int, int]:
    pulses: Queue[PulseTarget] = Queue()
    pulses.put(PulseTarget(Pulse.LOW, "button", "broadcaster"))
    low = 0
    high = 0

    while not pulses.empty():
        pulse_target: PulseTarget = pulses.get()
        if pulse_target.pulse == Pulse.LOW:
            low += 1
        else:
            high += 1

        module: BaseModule = modules[pulse_target.target]
        results: list[PulseTarget] = module.handle_pulse(
            pulse_target.src, pulse_target.pulse
        )
        for result in results:
            pulses.put(result)
    return low, high


def part1(module_map: dict[str, BaseModule]) -> None:
    low_total = 0
    high_total = 0
    for _ in range(1000):
        low, high = simulate(module_map)
        low_total += low
        high_total += high

    print(low_total, high_total)
    print(low_total * high_total)


def part2(module_map: dict[str, BaseModule]) -> None:
    modules: list[BaseModule] = list(module_map.values())
    os.makedirs("vis", exist_ok=True)

    for i in range(1024):
        graph_attr = {"labelloc": "t", "label": str(i)}
        dot = graphviz.Digraph(f"Push {i}", format="png", graph_attr=graph_attr)
        for module in modules:
            module.add_to_graph(dot)

        dot.render(directory="vis")
        simulate(module_map)

    # delete the gv stuff
    for item in os.listdir("vis"):
        if item.endswith(".gv"):
            os.remove(os.path.join("vis", item))


def main() -> None:
    modules = get_modules(FILE)
    modules = finalize_modules(modules)
    module_map = {module.name: module for module in modules}

    # q1
    part1(module_map)

    # q2
    part2(module_map)


if __name__ == "__main__":
    main()
