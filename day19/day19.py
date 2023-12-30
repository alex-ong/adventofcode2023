"""Day19 solution."""
from queue import Queue

from day19.lib.classes import Part, PartRange, PartRangeDest, Workflow
from day19.lib.parsers import parse_part_string, parse_workflow_string

"""
parsing classes section
"""
INPUT = "day19/input.txt"
INPUT_SMALL = "day19/input-small.txt"


def get_input(path: str) -> tuple[list[Workflow], list[Part]]:
    """Open file and parse.

    Returns well formed workflows and parts classes.

    Args:
        path (str): filepath for data

    Returns:
        tuple[list[Workflow], list[Part]]: list of workflows and parts.
    """
    workflows: list[Workflow] = []
    parts: list[Part] = []
    parsing_parts: bool = False
    with open(path, encoding="utf8") as file:
        for line in file:
            if len(line.strip()) == 0:
                parsing_parts = True
                continue
            if not parsing_parts:
                workflow: Workflow = parse_workflow_string(line)
                workflows.append(workflow)
            else:
                part: Part = parse_part_string(line)
                parts.append(part)
    return (workflows, parts)


def process_part(workflows: dict[str, Workflow], part: Part) -> int:
    """Processes a part.

    Returns the part rating (or 0 if rejected)

    Args:
        workflows (dict[str, Workflow]): list of workflows.
        part (Part): part to process

    Returns:
        int: value of part (or 0 if rejected)
    """
    # ends are `A` and R
    # start is `in`
    workflow = workflows["in"]
    while True:
        workflow_name = workflow.process_part(part)
        if workflow_name == "A":
            return part.rating
        if workflow_name == "R":
            return 0
        workflow = workflows[workflow_name]


def solve_part2(workflows: dict[str, Workflow]) -> int:
    """Solve part2.

    Assumes xmas values from 0 <= xmas <= 4000.
    Returns total number of parts that pass.

    Args:
        workflows (dict[str, Workflow]): workflows to test

    Returns:
        int: total number of parts that pass.
    """
    min_xmas = Part(1, 1, 1, 1)
    max_xmas = Part(4001, 4001, 4001, 4001)
    part_range = PartRange(min_xmas, max_xmas)

    starting_condition = PartRangeDest(part_range, "in")

    to_process: Queue[PartRangeDest] = Queue()
    to_process.put(starting_condition)
    result = 0
    while not to_process.empty():
        part_range_dest = to_process.get()
        part_range, dest = part_range_dest.part_range, part_range_dest.destination

        to_add: list[PartRangeDest] = workflows[dest].process_part_range(part_range)
        for item in to_add:
            if item.destination == "A":
                result += item.part_range.size()
            elif item.destination != "R":
                to_process.put(item)
    return result


def part1(workflows: list[Workflow], parts: list[Part]) -> int:
    """Solve part1."""
    workflows_mapping: dict[str, Workflow] = {wf.name: wf for wf in workflows}
    total = sum(process_part(workflows_mapping, part) for part in parts)

    return total


def part2(workflows: list[Workflow]) -> int:
    """Solve part2."""
    workflows_mapping: dict[str, Workflow] = {wf.name: wf for wf in workflows}
    return solve_part2(workflows_mapping)


def main() -> None:
    """Load input file and run part1/part2."""
    # combined
    workflows, parts = get_input(INPUT)

    print(part1(workflows, parts))
    print(part2(workflows))


if __name__ == "__main__":
    main()
