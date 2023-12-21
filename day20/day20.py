import math
import os
from queue import Queue

import graphviz
from lib.classes import (
    BaseModule,
    ConjunctionModule,
    FlipFlopModule,
    Pulse,
    PulseTarget,
)
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


def get_final_gates(module_map: dict[str, BaseModule]) -> list[ConjunctionModule]:
    """Should return vd, tp, pt, bk"""
    result: list[ConjunctionModule] = []
    for module in module_map.values():
        if isinstance(module, ConjunctionModule) and len(module.inputs) >= 8:
            result.append(module)
    print([module.name for module in result])
    return result


def get_switch_paths(
    start_switch: str, module_map: dict[str, BaseModule]
) -> list[BaseModule]:
    """given a start path, returns the longest path until we hit a conjunction module
    "" it should be n FlipFlops and then a single conjunction"""
    path: list[BaseModule] = []
    current_module: BaseModule = module_map[start_switch]
    while isinstance(current_module, FlipFlopModule):
        path.append(current_module)

        if len(current_module.outputs) == 1:
            current_module = module_map[current_module.outputs[0]]
        else:
            # return flipflop in outputs
            flipflops = (
                output
                for output in current_module.outputs
                if isinstance(module_map[output], FlipFlopModule)
            )
            current_module = module_map[next(flipflops)]

    path.append(current_module)  # should be a ConjunctionModule
    return path


def path_is_start_state(modules: list[BaseModule]) -> bool:
    """For every module in the path, make sure its in its "default" state"""
    return all(module.is_default_state() for module in modules)


def graph_modules(modules: list[BaseModule], index: int) -> None:
    """Graphs the modules"""
    graph_attr = {"labelloc": "t", "label": str(index)}
    dot = graphviz.Digraph(f"Push {index}", format="png", graph_attr=graph_attr)
    for module in modules:
        module.add_to_graph(dot)
    dot.render(directory="vis")


def part2(module_map: dict[str, BaseModule]) -> None:
    """We find out the loop length for each of the 4~ paths"""
    modules: list[BaseModule] = list(module_map.values())
    os.makedirs("vis", exist_ok=True)
    loops = module_map["broadcaster"].outputs

    switch_paths = [get_switch_paths(loop, module_map) for loop in loops]
    loop_lengths: dict[str, int] = {}

    # graph modules in initial state
    graph_modules(modules, 0)
    simulation_counter = 0

    # run simulation, screenshotting everytime one of the paths "loops"
    while len(loop_lengths) < len(switch_paths):
        simulate(module_map)
        simulation_counter += 1
        for switch_path in switch_paths:
            if path_is_start_state(switch_path):
                loop_end_name = switch_path[-1].name
                loop_lengths[loop_end_name] = simulation_counter
                graph_modules(modules, simulation_counter)
    print(loop_lengths)

    # Cleanup *.gv files
    for item in os.listdir("vis"):
        if item.endswith(".gv"):
            os.remove(os.path.join("vis", item))

    print(math.lcm(*list(loop_lengths.values())))


def main() -> None:
    modules = get_modules(FILE)
    modules = finalize_modules(modules)
    module_map = {module.name: module for module in modules}

    # q1
    # part1(module_map)

    # q2
    # MAKE SURE TO COMMENT OUT q1 for q2 to work!
    part2(module_map)


if __name__ == "__main__":
    main()
