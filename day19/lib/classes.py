"""well defined classes for day19."""
from dataclasses import dataclass
from enum import StrEnum
from typing import Optional


@dataclass
class Part:
    """Well defined part with x,m,a,s values."""

    x: int
    m: int
    a: int
    s: int

    @property
    def rating(self) -> int:
        """Returns rating of part (sum of xmas)."""
        return sum([self.x, self.m, self.a, self.s])

    def clone_modify(self, component: "Component", value: int) -> "Part":
        """Clones this part and modifies one component.

        Args:
            component (Component): component to change
            value (int): new value of component

        Returns:
            Part: clone of this part with one component changed.
        """
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
        """Returns value of a component inside this part."""
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
    """A well defined component inside a part."""

    X = "x"
    M = "m"
    A = "a"
    S = "s"


@dataclass
class PartRange:
    """A range of parts (min/max) based on component values."""

    min_values: Part  # from
    max_values: Part  # to, non-inclusive

    def size(self) -> int:
        """Returns the size of the partrange."""
        return (
            (self.max_values.x - self.min_values.x)
            * (self.max_values.m - self.min_values.m)
            * (self.max_values.a - self.min_values.a)
            * (self.max_values.s - self.min_values.s)
        )

    def split(
        self, component: Component, split_value: int
    ) -> tuple[Optional["PartRange"], Optional["PartRange"]]:
        """Split a partrange in two, using a chosen component and splitvalue.

        In the case that our range falls on one whole side, we return None.
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
        """Compact string representing our range."""
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
    """Combinatoin of partrange and a destination workflow."""

    part_range: PartRange
    destination: str

    def __str__(self) -> str:
        """Compact string representation."""
        return self.destination + ":" + str(self.part_range)


class Comparator(StrEnum):
    """Well defined comparators ``<`` and ``>``."""

    LessThan = "<"
    GreaterThan = ">"


@dataclass
class Condition:
    """A condition for a part to succeed/fail."""

    component: Component
    sign: Comparator
    value: int

    def process_part(self, part: Part) -> bool:
        """Checks a part to see if it matches our condition.

        Args:
            part (Part): part to check

        Raises:
            AssertionError: if component/sign are unsupported

        Returns:
            bool: True if the part passes our condition.
        """
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
        """Splits a part range based on success/fail.

        Args:
            part_range (PartRange): Partrange to check.

        Raises:
            AssertionError: If we have an unknown comparator

        Returns:
            tuple[Optional[PartRange], Optional[PartRange]]: successful part range, failed partrange
        """
        if self.sign == Comparator.LessThan:
            success, fail = part_range.split(self.component, self.value)
            return (success, fail)
        if self.sign == Comparator.GreaterThan:
            fail, success = part_range.split(self.component, self.value + 1)
            return (success, fail)
        raise AssertionError(f"Unknown comparator: {self.sign}")


@dataclass
class Rule:
    """A Rule consists of a condition + destination."""

    destination: str
    condition: Condition | None = None

    def process_part(self, part: Part) -> str | None:
        """Processes a part.

        Returns next workflow if successful,
        or None if we failed this rule
        """
        if self.condition is None:  # always pass
            return self.destination
        if self.condition.process_part(part):
            return self.destination
        return None

    def process_part_range(
        self, part_range: PartRange
    ) -> tuple[Optional[PartRangeDest], Optional[PartRange]]:
        """Processes a PartRange.

        Returns next workflow and partrange for succeeding parts.
        Returns the remainder partrange that failed.

        Args:
            part_range (PartRange): base partrange.

        Returns:
            tuple[Optional[PartRangeDest], Optional[PartRange]]: success, fail
        """
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
    """The name of the workflow + a bunch of rules for parts to follow."""

    name: str
    rules: list[Rule]

    def process_part(self, part: Part) -> str:
        """Processes a part, returns the next workflow."""
        for rule in self.rules:
            destination = rule.process_part(part)
            if destination is not None:
                return destination
        raise AssertionError("uh oh, hit the end of workflow!")

    def process_part_range(self, part_range: PartRange) -> list[PartRangeDest]:
        """Follow rule list, splitting off PartRanges.

        Each success has to branch off.
        Each failure continues down the chain.
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
