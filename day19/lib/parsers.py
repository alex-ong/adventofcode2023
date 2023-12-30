"""functions to create classes from pure text."""

from day19.lib.classes import Comparator, Component, Condition, Part, Rule, Workflow


def parse_part_string(part_string: str) -> Part:
    r"""Returns a part from a string representation.

    e.g. ``{x=787,m=2655,a=1222,s=2876}\n``
    """
    part_string = part_string.strip()
    part_string = part_string[1:-1]
    # Remove curly braces and split the string into key-value pairs
    key_value_pairs = part_string.split(",")

    # Create a dictionary from the key-value pairs
    part_dict = {}
    for pair in key_value_pairs:
        key, value = pair.split("=")
        part_dict[key.strip()] = int(value)

    # Create a Part instance using the dictionary
    return Part(**part_dict)


def parse_workflow_string(workflow_string: str) -> Workflow:
    r"""Returns a workflow from a string representation.

    e.g. ``px{a<2006:qkq,m>2090:A,rfg}\n``
    """
    workflow_string = workflow_string.strip()
    rule_start = workflow_string.index("{")
    name = workflow_string[:rule_start]
    rules_str = workflow_string[rule_start + 1 : -1]
    rule_strs = rules_str.split(",")
    rules: list[Rule] = [parse_rule_string(rule_str) for rule_str in rule_strs]

    return Workflow(name, rules)


def parse_rule_string(rule_string: str) -> Rule:
    """e.g. ``a<2006:qkq`` or ``rfg``."""
    dest_split = rule_string.split(":")
    if len(dest_split) == 1:
        return Rule(dest_split[0])
    else:
        condition = parse_condition_string(dest_split[0])
        return Rule(dest_split[1], condition)


def parse_condition_string(cond_string: str) -> Condition:
    """e.g. ``a<2006``."""
    component = Component(cond_string[0])
    operator = Comparator(cond_string[1])
    value = int(cond_string[2:])
    return Condition(component, operator, value)
