"""parsers"""
from day19.lib.classes import Comparator, Component, Condition, Part, Rule, Workflow
from day19.lib.parsers import (
    parse_condition_string,
    parse_part_string,
    parse_rule_string,
    parse_workflow_string,
)


def test_parse_part_string() -> None:
    part: Part = parse_part_string("{x=787,m=2655,a=1222,s=2876}\n")
    assert part == Part(787, 2655, 1222, 2876)

    part = parse_part_string("{x=1,m=2,a=3,s=4}\n")
    assert part == Part(1, 2, 3, 4)


def test_parse_workflow_string() -> None:
    """
    returns a workflow from a string representation
    `px{a<2006:qkq,m>2090:A,rfg}\n`
    """
    workflow: Workflow = parse_workflow_string("px{a<2006:qkq,m>2090:A,rfg}\n")
    rules = [
        Rule("qkq", Condition(Component.A, Comparator.LessThan, 2006)),
        Rule("A", Condition(Component.M, Comparator.GreaterThan, 2090)),
        Rule("rfg", None),
    ]
    workflow2 = Workflow("px", rules)
    assert workflow == workflow2  # confirm that workflow.eq works
    assert workflow.name == workflow2.name
    assert workflow.rules[0] == workflow2.rules[0]
    assert workflow.rules[1] == workflow2.rules[1]
    assert workflow.rules[2] == workflow2.rules[2]
    assert workflow.rules == workflow2.rules


def test_parse_rule_string() -> None:
    """
    `a<2006:qkq` or `rfg`
    """
    rule: Rule = parse_rule_string("a<2006:qkq")
    rule2: Rule = Rule("qkq", Condition(Component.A, Comparator.LessThan, 2006))

    assert rule.destination == rule2.destination
    assert rule.condition == rule2.condition
    assert rule == rule2

    rule = parse_rule_string("rfg")
    rule2 = Rule("rfg")

    assert rule.destination == rule2.destination
    assert rule.condition == rule2.condition
    assert rule == rule2


def test_parse_condition_string() -> None:
    """a<2006"""
    condition: Condition = parse_condition_string("a<2006")
    condition2: Condition = Condition(Component.A, Comparator.LessThan, 2006)
    assert condition == condition2
    assert condition.component == condition2.component
    assert condition.sign == condition2.sign
    assert condition.value == condition2.value
