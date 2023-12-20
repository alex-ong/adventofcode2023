from collections import defaultdict

from lib.classes import BaseModule, BroadcastModule, ConjunctionModule, FlipFlopModule


def parse_line(line: str) -> BaseModule:
    """
    %a -> inv, con
    """
    module_type_name, destinations = line.strip().split(" -> ")
    destination_list: list[str] = destinations.split(", ")
    if module_type_name == "broadcaster":
        return BroadcastModule("broadcaster", destination_list)
    module_name = module_type_name[1:]
    if module_type_name.startswith("%"):
        return FlipFlopModule(module_name, destination_list)
    if module_type_name.startswith("&"):
        return ConjunctionModule(module_name, destination_list)
    raise ValueError(f"Unparsable line: {line}")


def get_modules(filename: str) -> list[BaseModule]:
    modules: list[BaseModule] = []
    with open(filename, encoding="utf8") as file:
        for line in file:
            if len(line.strip()) == 0:
                break
            module: BaseModule = parse_line(line)
            modules.append(module)

    return modules


def set_inputs(modules: list[BaseModule]) -> None:
    """
    for each module, calculate its inputs.
    Then inject the inputs into our conjunction modules
    """
    inputs: dict[str, list[str]] = defaultdict(list)

    for module in modules:
        for output in module.outputs:
            inputs[output].append(module.name)

    for module in modules:
        if isinstance(module, ConjunctionModule):
            module.set_inputs(inputs[module.name])
