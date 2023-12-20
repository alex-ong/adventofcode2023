from dataclasses import dataclass, field
from enum import Flag

from graphviz import Digraph


class Pulse(Flag):
    LOW = False
    HIGH = True

    def __str__(self) -> str:
        if self.name is None:
            raise ValueError("no valid value for this Pulse")
        return self.name.lower()


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
        return f"{self.src} -{self.pulse}-> {self.target} "


@dataclass
class BaseModule:
    name: str
    outputs: list[str] = field(repr=False)
    num_low: int = 0
    num_high: int = 0

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        if pulse == Pulse.LOW:
            self.num_low += 1
        else:
            self.num_high += 1
        return []

    def add_to_graph(self, dot: Digraph) -> None:
        """adds edges only to the graph. inheritors need to handle their repr"""

        for output in self.outputs:
            dot.edge(self.name, output)


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
        dot.node(self.name)
        dot.attr()
        super().add_to_graph(dot)


@dataclass
class ConjunctionModule(BaseModule):
    """
    Keeps track of all inputs.
    Changes internal state, then sends high/low based on internal state
    """

    inputs: dict[str, Pulse] = field(init=False, repr=False)

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
        dot.node(self.name)
        super().add_to_graph(dot)


@dataclass
class BroadcastModule(BaseModule):
    """Broadcasts to all outputs"""

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        super().handle_pulse(input, pulse)
        return [PulseTarget(pulse, self.name, target) for target in self.outputs]

    def add_to_graph(self, dot: Digraph) -> None:
        dot.node(self.name)
        super().add_to_graph(dot)


@dataclass
class SinkModule(BaseModule):
    """Sink module, gets something but sents it no where else"""

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        super().handle_pulse(input, pulse)
        return []

    def add_to_graph(self, dot: Digraph) -> None:
        dot.node(self.name)
        super().add_to_graph(dot)
