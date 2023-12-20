from queue import Queue

from lib.classes import BaseModule, Pulse, PulseTarget
from lib.parsers_20 import finalize_modules, get_modules

FILE_A = "input-a.txt"
FILE_B = "input-b.txt"
FILE_PROD = "input.txt"

FILE = FILE_PROD


def simulate(modules: dict[str, BaseModule]) -> tuple[int, int]:
    pulses: Queue[PulseTarget] = Queue()
    pulses.put(PulseTarget(Pulse.LOW, "button", "broadcaster"))
    low = 0
    high = 0
    while not pulses.empty():
        pulse_target: PulseTarget = pulses.get()
        if pulse_target.pulse == Pulse.LOW:
            low += 1
        else:
            high += 1
        print(pulse_target)
        module: BaseModule = modules[pulse_target.target]
        results: list[PulseTarget] = module.handle_pulse(
            pulse_target.src, pulse_target.pulse
        )
        for result in results:
            pulses.put(result)
    return low, high


def main() -> None:
    modules = get_modules(FILE)
    modules = finalize_modules(modules)
    print("module listing:")
    for module in modules:
        print(module)
    module_map = {module.name: module for module in modules}

    low_total = 0
    high_total = 0
    for _ in range(1000):
        low, high = simulate(module_map)
        low_total += low
        high_total += high
    print(low_total, high_total)
    print(low_total * high_total)


if __name__ == "__main__":
    main()
