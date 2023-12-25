from collections import defaultdict

from day20.lib.classes import (
    BaseModule,
    BroadcastModule,
    ConjunctionModule,
    FlipFlopModule,
    SinkModule,
)


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

    modules = finalize_modules(modules)
    return modules


def finalize_modules(modules: list[BaseModule]) -> list[BaseModule]:
    """
    for each module, calculate its inputs.
    Then inject the inputs into our conjunction modules
    Modifies `modules` inplace, and returns it
    """
    inputs: dict[str, list[str]] = defaultdict(list)

    all_module_names: set[str] = set()
    for module in modules:
        for output in module.outputs:
            inputs[output].append(module.name)
            all_module_names.add(output)
            all_module_names.add(module.name)

    # add inputs to all conjunctions, find out missing outputs
    for module in modules:
        if isinstance(module, ConjunctionModule):
            module.set_inputs(inputs[module.name])
        all_module_names.remove(module.name)

    for item in all_module_names:
        module = SinkModule(item, [])
        modules.append(module)

    return modules
