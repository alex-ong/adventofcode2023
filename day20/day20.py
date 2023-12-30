"""Day20 solution."""
import math
import os
import shutil
from queue import Queue
from typing import Optional, Type, TypeVar, cast

import graphviz
from tqdm.contrib.concurrent import process_map

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
from day20.lib.parsers import get_modules

FILE_A = "day20/input-a.txt"
FILE_B = "day20/input-b.txt"
FILE_PT2 = "day20/input-test2.txt"
FILE_PROD = "day20/input.txt"

FILE = FILE_PROD
VIS_FOLDER = "day20/vis"
EXPORT_GRAPHS = False


def simulate(
    modules: dict[str, BaseModule], stored_pulses: Optional[list[PulseTarget]] = None
) -> tuple[int, int]:
    """Simulate a list of modules.

    If you pass in stored_pulses, we will append every pulse to it
    """
    pulses: Queue[PulseTarget] = Queue()
    pulses.put(PulseTarget(Pulse.LOW, "button", "broadcaster"))
    low = 0
    high = 0

    while not pulses.empty():
        pulse_target: PulseTarget = pulses.get()
        if stored_pulses is not None:
            stored_pulses.append(pulse_target)
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


def get_loop_paths(
    start_switch: str, module_map: dict[str, BaseModule]
) -> list[BaseModule]:
    """Given a start path, returns the longest path until we hit a conjunction module.

    It should be n FlipFlops and then a single conjunction
    """
    path: list[BaseModule] = []
    current_module: BaseModule = module_map[start_switch]
    while isinstance(current_module, FlipFlopModule):
        path.append(current_module)

        if len(current_module.outputs) == 1:
            current_module = module_map[current_module.outputs[0]]
        else:
            # return flipflop in outputs
            outputs: list[BaseModule] = [
                module_map[output] for output in current_module.outputs
            ]
            filtered = [node for node in outputs if isinstance(node, FlipFlopModule)]
            assert len(filtered) == 1
            current_module = filtered[0]

    path.append(current_module)  # should be a ConjunctionModule
    assert isinstance(current_module, ConjunctionModule)
    return path


def path_is_start_state(modules: list[BaseModule]) -> bool:
    """For every module in the path, make sure its in its "initial" state."""
    return all(module.is_initial_state() for module in modules)


T = TypeVar("T", bound=BaseModule)


def get_typed_module(
    module_map: dict[str, BaseModule], key: str, module_type: Type[T]
) -> T:
    """Typecast a module."""
    return cast(T, module_map[key])


def get_module_groups(module_map: dict[str, BaseModule]) -> ModuleGroups:
    """Splits the modules into their respective pipelines."""
    broadcaster = get_typed_module(module_map, "broadcaster", BroadcastModule)

    loop_paths = [
        get_loop_paths(node_name, module_map) for node_name in broadcaster.outputs
    ]
    loop_tails: list[ConjunctionModule] = []

    # for each loop, the conjunction module goes to one other conjunction.
    # grab this set of conjunctions, they are known as loop_tails
    for loop_path in loop_paths:
        last_node = loop_path[-1]

        nodes = [module_map[node_name] for node_name in last_node.outputs]
        filtered = [node for node in nodes if isinstance(node, ConjunctionModule)]
        assert len(filtered) == 1
        loop_tails.extend(filtered)

    last_join_name = loop_tails[0].outputs[0]
    last_conjunction = get_typed_module(module_map, last_join_name, ConjunctionModule)
    sink = get_typed_module(module_map, "rx", SinkModule)

    return ModuleGroups(broadcaster, loop_paths, loop_tails, last_conjunction, sink)


def graph_modules(module_groups: ModuleGroups, index: int) -> graphviz.Digraph:
    """Graphs the modules."""
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


def export_graph(
    dots: list[graphviz.Graph],
    module_groups: ModuleGroups,
    simulation_counter: int,
    export_graphs: bool,
) -> None:
    """Export a graphviz datatype if graphing is enabled."""
    if export_graphs:
        dot = graph_modules(module_groups, simulation_counter)
        dots.append(dot)


def part2(
    modules: list[BaseModule], export_graphs: bool = False
) -> tuple[int, list[graphviz.Graph]]:
    """We find out the loop length for each of the 4~ paths."""
    module_map = {module.name: module for module in modules}
    module_groups: ModuleGroups = get_module_groups(module_map)

    # graph modules in initial state
    dots: list[graphviz.Graph] = []
    simulation_counter = 0
    loop_counter: LoopCounter = LoopCounter(len(module_groups.loops))

    # output our initial state:
    export_graph(dots, module_groups, simulation_counter, export_graphs)

    # run simulation, screenshotting everytime one of the paths "loops"
    while not loop_counter.finished:
        simulate(module_map)
        simulation_counter += 1
        for loop_path in module_groups.loops:
            if path_is_start_state(loop_path):
                loop_end_name = loop_path[-1].name
                loop_counter.add_result(loop_end_name, simulation_counter)
        export_graph(dots, module_groups, simulation_counter, export_graphs)

    print(loop_counter)
    result = math.lcm(*list(loop_counter.loop_lengths.values()))
    return result, dots


def part1(modules: list[BaseModule]) -> int:
    """Counts low/high count for each module."""
    module_map = {module.name: module for module in modules}
    low_total = 0
    high_total = 0
    for _ in range(1000):
        low, high = simulate(module_map)
        low_total += low
        high_total += high

    print(low_total, high_total)
    return low_total * high_total


def output_graph(dot: graphviz.Graph, directory: str) -> None:
    """Saves a dot to file."""
    dot.render(directory=directory)


def output_graph_wrapper(args: tuple[graphviz.Graph, str]) -> None:
    """Since process_map doesnt support star_args, we gotta use this."""
    dot, directory = args
    output_graph(dot, directory)


def output_files(dots: list[graphviz.Graph], directory: str) -> None:
    """Saves a list of dots to file."""
    if len(dots) == 0:
        return
    shutil.rmtree(directory, ignore_errors=True)
    os.makedirs(directory, exist_ok=True)
    dot_dirs = [(dot, directory) for dot in dots]
    process_map(output_graph_wrapper, dot_dirs, chunksize=4)  # type: ignore

    # Cleanup *.gv files
    for item in os.listdir(directory):
        if item.endswith(".gv"):
            os.remove(os.path.join(directory, item))


def main() -> None:
    """Loads data from file then runs part1/part2."""
    modules = get_modules(FILE)
    # q1
    print(part1(modules))

    # q2
    # Reload because part1 ruins stuff

    modules = get_modules(FILE)
    result, dots = part2(modules, EXPORT_GRAPHS)
    print(result)
    output_files(dots, VIS_FOLDER)


if __name__ == "__main__":
    main()
