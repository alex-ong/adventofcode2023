from queue import Queue

from day19.lib.classes import Part, PartRange, PartRangeDest, Workflow
from day19.lib.parsers import parse_part_string, parse_workflow_string

"""
parsing classes section
"""


def get_input() -> tuple[list[Workflow], list[Part]]:
    workflows: list[Workflow] = []
    parts: list[Part] = []
    with open("day19/input.txt", encoding="utf8") as file:
        for line in file:
            if len(line.strip()) == 0:
                break
            workflow: Workflow = parse_workflow_string(line)
            workflows.append(workflow)

        for line in file:
            part: Part = parse_part_string(line)
            parts.append(part)
    return (workflows, parts)


def process_part(workflows: dict[str, Workflow], part: Part) -> bool:
    # ends are `A` and R
    # start is `in`
    workflow = workflows["in"]
    while True:
        workflow_name = workflow.process_part(part)
        if workflow_name == "A":
            return True
        if workflow_name == "R":
            return False
        workflow = workflows[workflow_name]


def solve_part2(workflows: dict[str, Workflow]) -> None:
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
    print(result)


def main() -> None:
    # combined
    workflows, parts = get_input()
    workflows_mapping: dict[str, Workflow] = {wf.name: wf for wf in workflows}

    # part 1
    total = 0
    for part in parts:
        if process_part(workflows_mapping, part):
            total += part.rating
    print(total)

    # part 2
    solve_part2(workflows_mapping)


if __name__ == "__main__":
    main()
