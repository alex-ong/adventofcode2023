from dataclasses import dataclass, field
from enum import Enum


def get_input():
    with open("input.txt") as file:
        return file.read()


def get_string_hash(string: str) -> int:
    value: int = 0
    for char in string:
        if char == "\n":
            continue
        value += ord(char)
        value *= 17
        value %= 256
    return value


class AddRemove(Enum):
    """Simple instruction to add or remove lens"""

    Add = 0
    Remove = 1


@dataclass
class Step:
    """well defined step"""

    lens_name: str
    box: int
    focal_length: int | None = None
    process: AddRemove | None = None


@dataclass
class Lens:
    """Lens object"""

    name: str
    focal_length: int

    def __hash__(self):
        return hash(str(self.name) + ":" + str(self.focal_length))

    def __str__(self):
        return f"[{self.name} {self.focal_length}]"


@dataclass
class Box:
    id: int = 0
    contents: list[Lens] = field(default_factory=list)

    def add_lens(self, lens: Lens):
        """
        If a lens name already exists, swap its power;
        otherwise just add it
        """
        for existing_lens in self.contents:
            if lens.name == existing_lens.name:
                existing_lens.focal_length = lens.focal_length
                return
        self.contents.append(lens)

    def remove_lens(self, lens: Lens):
        """if a lens with a matching name is inside, remove it"""
        to_remove = None
        for existing_lens in self.contents:
            if existing_lens.name == lens.name:
                to_remove = existing_lens
                break
        if to_remove is not None:
            self.contents.remove(to_remove)

    def __str__(self):
        return f"Box {self.id}: " + " ".join(str(lens) for lens in self.contents)

    def calculate_power(self):
        result = 0
        for slot_number, lens in enumerate(self.contents):
            box_power = 1 + self.id
            slot_power = slot_number + 1
            power = box_power * slot_power * lens.focal_length
            result += power

        return result


def parse_step_pt2(raw_step: str):
    """Handles as step in part 2"""
    print(raw_step)
    if len(splits := raw_step.split("=")) == 2:
        box = get_string_hash(splits[0])
        strength = int(splits[1].strip())
        return Step(splits[0], box, strength, AddRemove.Add)
    elif len(splits := raw_step.split("-")) == 2:
        box = get_string_hash(splits[0])
        return Step(splits[0], box, process=AddRemove.Remove)

    raise ValueError(raw_step)


def print_boxes(boxes: list[Box]):
    for box in boxes:
        if len(box.contents) > 0:
            print(box)


def process_steps_pt2(steps: list[Step]):
    boxes: list[Box] = [Box(i) for i in range(256)]
    lenses: dict[str, Lens] = {}
    for step in steps:
        if step.process == AddRemove.Remove:
            if step.lens_name in lenses:
                lens = lenses[step.lens_name]
                boxes[step.box].remove_lens(lens)
        else:
            if step.focal_length is None:
                raise ValueError("focal length should not be None")
            lens = Lens(step.lens_name, step.focal_length)
            boxes[step.box].add_lens(lens)
            lenses[lens.name] = lens
    return sum(box.calculate_power() for box in boxes)


def main():
    chars = get_input()
    raw_steps = chars.split(",")
    # q1
    print(sum(get_string_hash(raw_step) for raw_step in raw_steps))

    # q2
    steps = [parse_step_pt2(raw_step) for raw_step in raw_steps]
    print("\n".join(str(step) for step in steps))
    print(process_steps_pt2(steps))


if __name__ == "__main__":
    main()
