"""Tests for day19 classes."""
from day19.lib.classes import (
    Comparator,
    Component,
    Condition,
    Part,
    PartRange,
    PartRangeDest,
    Rule,
    Workflow,
)


def get_part_range() -> tuple[Part, Part]:
    """Returns a reusable partrange for our tests."""
    return Part(100, 100, 100, 100), Part(150, 200, 150, 150)


def test_part_range() -> None:
    """Test ``PartRange`` class."""
    low: Part = Part(100, 100, 100, 100)
    high: Part = Part(150, 200, 150, 150)
    part_range: PartRange = PartRange(low, high)
    low_split, high_split = part_range.split(Component.M, 300)
    assert low_split == part_range
    assert high_split is None

    low_split, high_split = part_range.split(Component.M, 25)
    assert low_split is None
    assert high_split == part_range

    assert str(part_range) == "100<=x<=149, 100<=m<=199, 100<=a<=149, 100<=s<=149"


def test_part_range_dest() -> None:
    """Test ``PartRangeDest`` class."""
    part_range: PartRange = PartRange(*get_part_range())
    part_range_dest = PartRangeDest(part_range, "test")
    assert (
        str(part_range_dest)
        == "test:100<=x<=149, 100<=m<=199, 100<=a<=149, 100<=s<=149"
    )


def test_rule() -> None:
    """Test ``Rule`` class."""
    rule = Rule("test", Condition(Component.M, Comparator.LessThan, 50))

    low: Part = Part(100, 100, 100, 100)
    high: Part = Part(150, 200, 150, 150)
    part_range = PartRange(low, high)
    dest, rest = rule.process_part_range(part_range)
    assert dest is None
    assert rest == part_range


def test_workflow() -> None:
    """Test ``Workflow`` class."""
    rule1: Rule = Rule("test", Condition(Component.M, Comparator.LessThan, 50))
    rule2: Rule = Rule("rest")
    workflow: Workflow = Workflow("workflow1", [rule1, rule2])

    low: Part = Part(100, 100, 100, 100)
    high: Part = Part(150, 200, 150, 150)
    part_range = PartRange(low, high)
    results = workflow.process_part_range(part_range)
    assert results[0].destination == "rest"
