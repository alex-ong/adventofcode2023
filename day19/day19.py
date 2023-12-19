from lib.classes import Part, Workflow
from lib.parsers import parse_part_string, parse_workflow_string

"""
parsing classes section
"""


def get_input() -> tuple[list[Workflow], list[Part]]:
    workflows: list[Workflow] = []
    parts: list[Part] = []
    with open("input-small.txt", encoding="utf8") as file:
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


def main() -> None:
    workflows, parts = get_input()

    workflows_mapping: dict[str, Workflow] = {wf.name: wf for wf in workflows}
    total = 0
    for part in parts:
        if process_part(workflows_mapping, part):
            total += part.rating
    print(total)


if __name__ == "__main__":
    main()
