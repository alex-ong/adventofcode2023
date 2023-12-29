from day15.lib.classes import AddRemove, Box, Lens, Step

INPUT = "day15/input.txt"
INPUT_SMALL = "day15/input-small.txt"


def get_input(path: str) -> list[str]:
    with open(path) as file:
        data = file.read()
    raw_steps = data.split(",")
    return raw_steps


def get_string_hash(string: str) -> int:
    value: int = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256
    return value


def parse_step_pt2(raw_step: str) -> Step:
    """Handles as step in part 2"""
    if len(splits := raw_step.split("=")) == 2:
        box = get_string_hash(splits[0])
        strength = int(splits[1].strip())
        return Step(splits[0], box, AddRemove.Add, strength)
    elif len(splits := raw_step.split("-")) == 2:
        box = get_string_hash(splits[0])
        return Step(splits[0], box, AddRemove.Remove)

    raise AssertionError("Raw step does not contain `-` or `=`")


def process_steps_pt2(steps: list[Step]) -> int:
    """Process a list of steps"""
    boxes: list[Box] = [Box(i) for i in range(256)]

    for step in steps:
        if step.process == AddRemove.Remove:
            boxes[step.box].remove_lens(step.lens_name)
        else:
            if step.focal_length is None:
                raise AssertionError("focal length should not be None")
            lens = Lens(step.lens_name, step.focal_length)
            boxes[step.box].add_lens(lens)

    return sum(box.calculate_power() for box in boxes)


def question1(raw_steps: list[str]) -> int:
    return sum(get_string_hash(raw_step) for raw_step in raw_steps)


def question2(raw_steps: list[str]) -> int:
    steps = [parse_step_pt2(raw_step) for raw_step in raw_steps]
    return process_steps_pt2(steps)


def main() -> None:
    """Main function"""
    raw_steps = get_input(INPUT)

    # q1
    print(question1(raw_steps))

    # q2
    print(question2(raw_steps))


if __name__ == "__main__":
    main()
