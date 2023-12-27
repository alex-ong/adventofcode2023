"""well defined classes"""
from dataclasses import dataclass
from enum import StrEnum
from typing import Optional


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @property
    def rating(self) -> int:
        return sum([self.x, self.m, self.a, self.s])

    def clone_modify(self, component: "Component", value: int) -> "Part":
        x, m, a, s = self.x, self.m, self.a, self.s
        if component == Component.X:
            x = value
        if component == Component.M:
            m = value
        if component == Component.A:
            a = value
        if component == Component.S:
            s = value

        return Part(x, m, a, s)

    def get_value(self, component: "Component") -> int:
        if component == Component.X:
            return self.x
        if component == Component.M:
            return self.m
        if component == Component.A:
            return self.a
        if component == Component.S:
            return self.s
        raise AssertionError(f"Unsupported component{component}")


class Component(StrEnum):
    X = "x"
    M = "m"
    A = "a"
    S = "s"


@dataclass
class PartRange:
    min_values: Part  # from
    max_values: Part  # to, non-inclusive

    def size(self) -> int:
        return (
            (self.max_values.x - self.min_values.x)
            * (self.max_values.m - self.min_values.m)
            * (self.max_values.a - self.min_values.a)
            * (self.max_values.s - self.min_values.s)
        )

    def split(
        self, component: Component, split_value: int
    ) -> tuple[Optional["PartRange"], Optional["PartRange"]]:
        """
        Split a partrange in two, using a chosen component and splitvalue
        in the case that our range falls on one whole side, we return None.
        E.g.
        range = 0-100; split == 200 -> return [(0-100), None]
        range = 100-200; split == 50 -> return [None, (100-200)]
        range = 100-200, split == 150 -> return [(100-150), (150-200)]
        """
        min_value = self.min_values.get_value(component)
        max_value = self.max_values.get_value(component)
        if split_value >= max_value:
            return (self, None)
        if split_value < min_value:
            return (None, self)

        mid_high = self.min_values.clone_modify(component, split_value)
        mid_low = self.max_values.clone_modify(component, split_value)

        return (
            PartRange(self.min_values, mid_low),
            PartRange(mid_high, self.max_values),
        )

    def __str__(self) -> str:
        return ", ".join(
            [
                f"{self.min_values.x}<=x<={self.max_values.x-1}",
                f"{self.min_values.m}<=m<={self.max_values.m-1}",
                f"{self.min_values.a}<=a<={self.max_values.a-1}",
                f"{self.min_values.s}<=s<={self.max_values.s-1}",
            ]
        )


@dataclass
class PartRangeDest:
    part_range: PartRange
    destination: str

    def __str__(self) -> str:
        return self.destination + ":" + str(self.part_range)


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
            raise AssertionError(f"Unsupported component: {self.component}")

        if self.sign == Comparator.GreaterThan:
            return part_val > self.value
        elif self.sign == Comparator.LessThan:
            return part_val < self.value
        else:
            raise AssertionError(f"Unsupported comparator: {self.sign}")

    def process_part_range(
        self, part_range: PartRange
    ) -> tuple[Optional[PartRange], Optional[PartRange]]:
        """return pass, fail as ranges"""
        if self.sign == Comparator.LessThan:
            success, fail = part_range.split(self.component, self.value)
            return (success, fail)
        if self.sign == Comparator.GreaterThan:
            fail, success = part_range.split(self.component, self.value + 1)
            return (success, fail)
        raise AssertionError(f"Unknown comparator: {self.sign}")


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

    def process_part_range(
        self, part_range: PartRange
    ) -> tuple[Optional[PartRangeDest], Optional[PartRange]]:
        success: Optional[PartRange]
        fail: Optional[PartRange]
        if self.condition is None:  # pass all
            success, fail = part_range, None
        else:  # split up range
            success, fail = self.condition.process_part_range(part_range)
        if success is not None:
            return (PartRangeDest(success, self.destination), fail)

        return None, fail


@dataclass(eq=True)
class Workflow:
    name: str
    rules: list[Rule]

    def process_part(self, part: Part) -> str:
        """processes a part, returns the next workflow"""
        for rule in self.rules:
            destination = rule.process_part(part)
            if destination is not None:
                return destination
        raise AssertionError("uh oh, hit the end of workflow!")

    def process_part_range(self, part_range: PartRange) -> list[PartRangeDest]:
        """
        Follow rule list. Each success has to branch off,
        each failure continues down the chain.
        """
        results: list[PartRangeDest] = []
        remainder: Optional[PartRange] = part_range

        index = 0
        while remainder is not None:
            rule = self.rules[index]
            success, remainder = rule.process_part_range(remainder)
            if success is not None:
                results.append(success)
            index += 1

        return results
