from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Flag


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
class BaseModule(ABC):
    name: str
    outputs: list[str]

    @abstractmethod
    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        pass


@dataclass
class FlipFlopModule(BaseModule):
    state: Pulse = Pulse.LOW

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        if pulse:
            return []
        # if we were low, become high and send high
        # if we were high, become low and send low

        self.state = Pulse(not self.state)
        return [PulseTarget(self.state, self.name, target) for target in self.outputs]


@dataclass
class ConjunctionModule(BaseModule):
    inputs: dict[str, Pulse] = field(init=False)

    def set_inputs(self, inputs: list[str]) -> None:
        self.inputs = {input_name: Pulse.LOW for input_name in inputs}

    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        self.inputs[input] = pulse
        if all(self.inputs.values()):
            return [
                PulseTarget(Pulse.LOW, self.name, target) for target in self.outputs
            ]
        return [PulseTarget(Pulse.HIGH, self.name, target) for target in self.outputs]


@dataclass
class BroadcastModule(BaseModule):
    def handle_pulse(self, input: str, pulse: Pulse) -> list[PulseTarget]:
        return [PulseTarget(pulse, self.name, target) for target in self.outputs]
