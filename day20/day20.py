import math
import os
from multiprocessing import Pool
from queue import Queue
from typing import Type, TypeVar, cast

import graphviz
import tqdm

from day20.lib.classes import (
    BaseModule,
    BroadcastModule,
    ConjunctionModule,
    FlipFlopModule,
    LoopCounter,
    ModuleGroups,
    Pulse,
    PulseTarget,
    SinkModule,
)
from day20.lib.parsers import finalize_modules, get_modules

FILE_A = "day21/input-a.txt"
FILE_B = "day21/input-b.txt"
FILE_PROD = "day21/input.txt"

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


def get_loop_paths(
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


T = TypeVar("T", bound=BaseModule)


def get_typed_module(
    module_map: dict[str, BaseModule], key: str, module_type: Type[T]
) -> T:
    return cast(T, module_map[key])


def get_module_groups(module_map: dict[str, BaseModule]) -> ModuleGroups:
    """Splits the modules into their respective pipelines"""
    broadcaster = get_typed_module(module_map, "broadcaster", BroadcastModule)

    loop_paths = [
        get_loop_paths(node_name, module_map) for node_name in broadcaster.outputs
    ]
    loop_tails: list[ConjunctionModule] = []
    for loop_path in loop_paths:
        last_node = loop_path[-1]
        for node_name in last_node.outputs:
            node = module_map[node_name]
            if isinstance(node, ConjunctionModule):
                loop_tails.append(node)
                break
    last_join_name = loop_tails[0].outputs[0]
    last_conjunction = get_typed_module(module_map, last_join_name, ConjunctionModule)
    sink = get_typed_module(module_map, "rx", SinkModule)

    return ModuleGroups(broadcaster, loop_paths, loop_tails, last_conjunction, sink)


def graph_modules(module_groups: ModuleGroups, index: int) -> graphviz.Digraph:
    """Graphs the modules"""

    index_str = str(index).zfill(4)
    graph_attr = {"labelloc": "t", "label": index_str}
    dot = graphviz.Digraph(f"Push {index_str}", format="png", graph_attr=graph_attr)

    # broadcaster
    with dot.subgraph(graph_attr={"rank": "source"}) as s:
        s.node(module_groups.head.name)

    # loop nodes
    for index in range(max(len(loop) for loop in module_groups.loops)):
        with dot.subgraph(graph_attr={"rank": "same"}) as s:
            s.attr(rank="same")
            for loop_path in module_groups.loops:
                if index < len(loop_path) - 1:
                    node = loop_path[index]
                    s.node(node.name)

    # loop tails
    with dot.subgraph(graph_attr={"rank": "same"}) as s:
        for node in module_groups.loop_tails:
            s.node(node.name)
    # penultimate
    with dot.subgraph(graph_attr={"rank": "same"}) as s:
        s.node(module_groups.penultimate.name)

    with dot.subgraph(graph_attr={"rank": "sink"}) as s:
        s.node(module_groups.sink.name)

    # now that we've done ranks, just add all of them with their arrows.
    for node in module_groups.all_nodes:
        node.add_to_graph(dot)

    return dot


def part2(module_map: dict[str, BaseModule]) -> None:
    """We find out the loop length for each of the 4~ paths"""
    module_groups: ModuleGroups = get_module_groups(module_map)
    os.makedirs("vis", exist_ok=True)

    # graph modules in initial state
    dots: list[graphviz.Graph] = []
    dot: graphviz.Graph = graph_modules(module_groups, 0)
    simulation_counter = 0
    loop_counter: LoopCounter = LoopCounter(len(module_groups.loops))
    # run simulation, screenshotting everytime one of the paths "loops"
    while not loop_counter.finished:
        simulate(module_map)
        simulation_counter += 1
        for loop_path in module_groups.loops:
            if path_is_start_state(loop_path):
                loop_end_name = loop_path[-1].name
                loop_counter.add_result(loop_end_name, simulation_counter)
        dot = graph_modules(module_groups, simulation_counter)
        dots.append(dot)

    print(loop_counter)
    print(math.lcm(*list(loop_counter.loop_lengths.values())))

    output_files(dots)

    # Cleanup *.gv files
    for item in os.listdir("vis"):
        if item.endswith(".gv"):
            os.remove(os.path.join("vis", item))


def output_graph(dot: graphviz.Graph) -> None:
    """Saves a dot to file"""
    dot.render(directory="vis")


def output_files(dots: list[graphviz.Graph]) -> None:
    """Saves a list of dots to file"""

    with Pool() as pool:
        for _ in tqdm.tqdm(pool.imap_unordered(output_graph, dots), total=len(dots)):
            pass

    print("all done!")


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
