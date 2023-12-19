from dataclasses import dataclass
from enum import StrEnum


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @property
    def rating(self) -> int:
        return sum([self.x, self.m, self.a, self.s])


class Component(StrEnum):
    X = "x"
    M = "m"
    A = "a"
    S = "s"


class Comparator(StrEnum):
    LessThan = "<"
    GreaterThan = ">"


@dataclass
class Condition:
    component: Component
    sign: Comparator
    value: int

    def process_part(self, part: Part) -> bool:
        part_val: int
        if self.component == Component.X:
            part_val = part.x
        elif self.component == Component.M:
            part_val = part.m
        elif self.component == Component.A:
            part_val = part.a
        elif self.component == Component.S:
            part_val = part.s
        else:
            raise ValueError(f"Unsupported component: {self.component}")

        if self.sign == Comparator.GreaterThan:
            return part_val > self.value
        elif self.sign == Comparator.LessThan:
            return part_val < self.value
        else:
            raise ValueError(f"Unsupported comparator: {self.sign}")


@dataclass
class Rule:
    destination: str
    condition: Condition | None = None

    def process_part(self, part: Part) -> str | None:
        """Processes a part. Returns next workflow if successful,
        or None if we failed this rule"""
        if self.condition is None:  # always pass
            return self.destination
        if self.condition.process_part(part):
            return self.destination
        return None


@dataclass
class Workflow:
    name: str
    rules: list[Rule]

    def process_part(self, part: Part) -> str:
        """processes a part, returns the next workflow"""
        for rule in self.rules:
            destination = rule.process_part(part)
            if destination is not None:
                return destination
        raise ValueError("uh oh, hit the end of worfkflow!")
