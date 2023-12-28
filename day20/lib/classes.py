import itertools
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Flag

from graphviz import Digraph


class Pulse(Flag):
    LOW = False
    HIGH = True

    def __str__(self) -> str:
        if self.name is not None:
            return self.name.lower()
        raise AssertionError("no valid value for this Pulse")


@dataclass
class MappingModule:
    name: str
    outputs: list[str]


@dataclass
class PulseTarget:
    pulse: Pulse
    src: str
    target: str

    def __str__(self) -> str:
        return f"{self.src} -{self.pulse}-> {self.target}"


@dataclass
class BaseModule(ABC):
    name: str
    outputs: list[str] = field(repr=False)
    num_low: int = field(init=False, default=0)
    num_high: int = field(init=False, default=0)

    def __post_init__(self) -> None:
        if self.__class__ == BaseModule:
            raise AssertionError("Cannot instantiate abstract class")

    def arrow_color(self) -> str:
        return "#000000"

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        if pulse == Pulse.LOW:
            self.num_low += 1
        else:
            self.num_high += 1
        return []

    def add_to_graph(self, dot: Digraph) -> None:
        """adds edges only to the graph. inheritors need to handle their repr"""
        attrs = {"color": self.arrow_color()}

        for output in self.outputs:
            dot.edge(self.name, output, **attrs)

    @abstractmethod
    def is_default_state(self) -> bool:
        raise AssertionError("Implement me")


@dataclass
class FlipFlopModule(BaseModule):
    """
    If we receive HIGH, we are a sink (do nothing)
    If we receive LOW, flip our current value and send it to everyone
    """

    state: Pulse = Pulse.LOW

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        super().handle_pulse(input, pulse)
        if pulse:
            return []
        # if we were low, become high and send high
        # if we were high, become low and send low

        self.state = Pulse(not self.state)
        return [PulseTarget(self.state, self.name, target) for target in self.outputs]

    def add_to_graph(self, dot: Digraph) -> None:
        attrs = {"shape": "box", "style": "filled"}
        if self.state == Pulse.LOW:
            attrs["fillcolor"] = "#FF0000"
        else:
            attrs["fillcolor"] = "#0000FF"
        dot.node(self.name, **attrs)
        super().add_to_graph(dot)

    def is_default_state(self) -> bool:
        return self.state == Pulse.LOW


@dataclass
class ConjunctionModule(BaseModule):
    """
    Keeps track of all inputs.
    Changes internal state, then sends high/low based on internal state
    """

    inputs: dict[str, Pulse] = field(init=False, repr=False)

    def arrow_color(self) -> str:
        return "#FF0000"

    def set_inputs(self, inputs: list[str]) -> None:
        self.inputs = {input_name: Pulse.LOW for input_name in inputs}

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        super().handle_pulse(input, pulse)
        self.inputs[input] = pulse
        if all(self.inputs.values()):
            return [
                PulseTarget(Pulse.LOW, self.name, target) for target in self.outputs
            ]
        return [PulseTarget(Pulse.HIGH, self.name, target) for target in self.outputs]

    def add_to_graph(self, dot: Digraph) -> None:
        count = self.current_count()
        length = len(list(self.inputs.values()))
        label = f"{self.name} {count}/{length}"
        dot.node(self.name, label=label)
        super().add_to_graph(dot)

    def current_count(self) -> int:
        return list(self.inputs.values()).count(Pulse.HIGH)

    def is_default_state(self) -> bool:
        return self.current_count() == 0


@dataclass
class BroadcastModule(BaseModule):
    """Broadcasts to all outputs"""

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        super().handle_pulse(input, pulse)
        return [PulseTarget(pulse, self.name, target) for target in self.outputs]

    def add_to_graph(self, dot: Digraph) -> None:
        dot.node(self.name)
        super().add_to_graph(dot)

    def is_default_state(self) -> bool:
        return True


@dataclass
class SinkModule(BaseModule):
    """Sink module, gets something but sends it no where else"""

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        super().handle_pulse(input, pulse)
        return []

    def add_to_graph(self, dot: Digraph) -> None:
        dot.node(self.name)
        super().add_to_graph(dot)

    def is_default_state(self) -> bool:
        return True


@dataclass
class ModuleGroups:
    head: BroadcastModule
    loops: list[list[BaseModule]]
    loop_tails: list[ConjunctionModule]
    penultimate: ConjunctionModule
    sink: SinkModule
    all_nodes: list[BaseModule] = field(init=False)

    def __post_init__(self) -> None:
        all_nodes: list[BaseModule] = []
        all_nodes.append(self.head)
        all_nodes.extend(list(itertools.chain(*self.loops)))
        all_nodes.extend(self.loop_tails)
        all_nodes.append(self.penultimate)
        all_nodes.append(self.sink)
        self.all_nodes = all_nodes


@dataclass
class LoopCounter:
    target_loop_count: int = field(repr=False)
    loop_lengths: dict[str, int] = field(default_factory=dict, init=False)

    @property
    def num_results(self) -> int:
        return len(self.loop_lengths)

    @property
    def finished(self) -> bool:
        return self.num_results == self.target_loop_count

    def add_result(self, loop_name: str, value: int) -> None:
        if loop_name not in self.loop_lengths:
            self.loop_lengths[loop_name] = value
