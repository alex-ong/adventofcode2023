from queue import Queue

from lib.classes import BaseModule, Pulse, PulseTarget
from lib.parsers_20 import get_modules, set_inputs

FILE_A = "input-a.txt"
FILE_B = "input-b.txt"
FILE_PROD = "input.txt"

FILE = FILE_B


def simulate(modules: dict[str, BaseModule]) -> None:
    pulses: Queue[PulseTarget] = Queue()
    pulses.put(PulseTarget(Pulse.LOW, "button", "broadcaster"))

    while not pulses.empty():
        pulse_target: PulseTarget = pulses.get()
        print(pulse_target)
        module: BaseModule = modules[pulse_target.target]
        results: list[PulseTarget] = module.handle_pulse(
            pulse_target.src, pulse_target.pulse
        )
        for result in results:
            pulses.put(result)


def main() -> None:
    modules = get_modules(FILE)
    set_inputs(modules)
    print("module listing:")
    for module in modules:
        print(module)
    module_map = {module.name: module for module in modules}

    count = 0
    while True:
        print(f"simulating... {count}")
        simulate(module_map)
        should_continue = input()
        if should_continue.startswith("n"):
            return
        count += 1


if __name__ == "__main__":
    main()
