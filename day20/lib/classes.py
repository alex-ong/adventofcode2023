"""Classes for day20."""
import itertools
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Flag

from graphviz import Digraph


class Pulse(Flag):
    """Simple True/False enum."""

    LOW = False
    HIGH = True

    def __str__(self) -> str:
        """Custom str to show ``low`` and ``high``."""
        if self.name is not None:
            return self.name.lower()
        raise AssertionError("no valid value for this Pulse")


@dataclass
class MappingModule:
    """map to a list of outputs."""

    name: str
    outputs: list[str]


@dataclass
class PulseTarget:
    """A pulse(low/high) from src to dest."""

    pulse: Pulse
    src: str
    target: str

    def __str__(self) -> str:
        """Custom arrow string to match problem description."""
        return f"{self.src} -{self.pulse}-> {self.target}"


@dataclass
class BaseModule(ABC):
    """Abstract base module."""

    name: str
    outputs: list[str] = field(repr=False)
    num_low: int = field(init=False, default=0)
    num_high: int = field(init=False, default=0)

    def __post_init__(self) -> None:
        """Stop users from constructing BaseModule."""
        if self.__class__ == BaseModule:
            raise AssertionError("Cannot instantiate abstract class")

    def arrow_color(self) -> str:
        """Return arrow color for graphviz."""
        return "#000000"

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        """Keep track of lows/highs through all modules."""
        if pulse == Pulse.LOW:
            self.num_low += 1
        else:
            self.num_high += 1
        return []

    def add_to_graph(self, dot: Digraph) -> None:
        """Adds edges only to the graph. inheritors need to handle their repr."""
        attrs = {"color": self.arrow_color()}

        for output in self.outputs:
            dot.edge(self.name, output, **attrs)

    @abstractmethod
    def is_initial_state(self) -> bool:
        """Returns if the module is in the initial state."""
        raise AssertionError("Implement me")


@dataclass
class FlipFlopModule(BaseModule):
    """If we receive HIGH, we are a sink (do nothing).

    If we receive LOW, flip our current value and send it to everyone
    """

    state: Pulse = Pulse.LOW

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        """Handle pulse by forwarding if we receive low."""
        super().handle_pulse(input, pulse)
        if pulse:
            return []
        # if we receive low, become the opposite and send it.
        # if we receive high, do ont send, do not modify state.

        self.state = Pulse(not self.state)
        return [PulseTarget(self.state, self.name, target) for target in self.outputs]

    def add_to_graph(self, dot: Digraph) -> None:
        """Adds ourselves to a graphviz digraph."""
        attrs = {"shape": "box", "style": "filled"}
        if self.state == Pulse.LOW:
            attrs["fillcolor"] = "#FF0000"
        else:
            attrs["fillcolor"] = "#0000FF"
        dot.node(self.name, **attrs)
        super().add_to_graph(dot)

    def is_initial_state(self) -> bool:
        """Returns true if we are in our initial state."""
        return self.state == Pulse.LOW


@dataclass
class ConjunctionModule(BaseModule):
    """Keeps track of all inputs.

    Changes internal state, then sends high/low based on internal state
    """

    inputs: dict[str, Pulse] = field(init=False, repr=False)

    def arrow_color(self) -> str:
        """Returns red."""
        return "#FF0000"

    def set_inputs(self, inputs: list[str]) -> None:
        """Sets our list of input modules.

        Initializes their values to Low.
        """
        self.inputs = {input_name: Pulse.LOW for input_name in inputs}

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        """Store pulse, then send based on current state.

        If all our values are high, we send low to all our outputs.
        Otherwise, we send ``LOW`` to all our outputs.
        """
        super().handle_pulse(input, pulse)
        self.inputs[input] = pulse
        if all(self.inputs.values()):
            return [
                PulseTarget(Pulse.LOW, self.name, target) for target in self.outputs
            ]
        return [PulseTarget(Pulse.HIGH, self.name, target) for target in self.outputs]

    def add_to_graph(self, dot: Digraph) -> None:
        """Add this module to a GraphViz Digraph."""
        count = self.current_count()
        length = len(list(self.inputs.values()))
        label = f"{self.name} {count}/{length}"
        dot.node(self.name, label=label)
        super().add_to_graph(dot)

    def current_count(self) -> int:
        """Returns current count of inputs that sent ``high``."""
        return list(self.inputs.values()).count(Pulse.HIGH)

    def is_initial_state(self) -> bool:
        """Returns True if all our inputs are LOW."""
        return self.current_count() == 0


@dataclass
class BroadcastModule(BaseModule):
    """Broadcasts to all outputs."""

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        """Broadcasts to all outputs immediately."""
        super().handle_pulse(input, pulse)
        return [PulseTarget(pulse, self.name, target) for target in self.outputs]

    def add_to_graph(self, dot: Digraph) -> None:
        """Add node to graphviz digraph."""
        dot.node(self.name)
        super().add_to_graph(dot)

    def is_initial_state(self) -> bool:
        """Always true."""
        return True


@dataclass
class SinkModule(BaseModule):
    """Sink module, gets something but sends it no where else."""

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        """Always eats inputs and never sends onwards."""
        super().handle_pulse(input, pulse)
        return []

    def add_to_graph(self, dot: Digraph) -> None:
        """Adds this node to the graph."""
        dot.node(self.name)
        super().add_to_graph(dot)

    def is_initial_state(self) -> bool:
        """Always true."""
        return True


@dataclass
class ModuleGroups:
    """A group of modules for part2."""

    head: BroadcastModule
    loops: list[list[BaseModule]]
    loop_tails: list[ConjunctionModule]
    penultimate: ConjunctionModule
    sink: SinkModule
    all_nodes: list[BaseModule] = field(init=False)

    def __post_init__(self) -> None:
        """Sets up our ``all_nodes`` property."""
        all_nodes: list[BaseModule] = []
        all_nodes.append(self.head)
        all_nodes.extend(list(itertools.chain(*self.loops)))
        all_nodes.extend(self.loop_tails)
        all_nodes.append(self.penultimate)
        all_nodes.append(self.sink)
        self.all_nodes = all_nodes


@dataclass
class LoopCounter:
    """Keeps track of loop lengths."""

    target_loop_count: int = field(repr=False)
    loop_lengths: dict[str, int] = field(default_factory=dict, init=False)

    @property
    def num_results(self) -> int:
        """Returns number of loop_lenghts submitted."""
        return len(self.loop_lengths)

    @property
    def finished(self) -> bool:
        """Returns True if our loop_lengths are equal to our target."""
        return self.num_results == self.target_loop_count

    def add_result(self, loop_name: str, value: int) -> None:
        """Adds a result to our loop_count.

        If we already had a loop with that name, we ignore it.
        """
        if loop_name not in self.loop_lengths:
            self.loop_lengths[loop_name] = value
