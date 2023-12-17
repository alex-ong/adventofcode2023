from dataclasses import dataclass, field
from enum import Enum


def get_input() -> str:
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

    def __hash__(self) -> int:
        return hash(str(self.name) + ":" + str(self.focal_length))

    def __str__(self) -> str:
        return f"[{self.name} {self.focal_length}]"


@dataclass
class Box:
    id: int = 0
    contents: list[Lens] = field(default_factory=list)

    def add_lens(self, lens: Lens) -> None:
        """
        If a lens name already exists, swap its power;
        otherwise just add it
        """
        for existing_lens in self.contents:
            if lens.name == existing_lens.name:
                existing_lens.focal_length = lens.focal_length
                return
        self.contents.append(lens)

    def remove_lens(self, lens_name: str) -> None:
        """if a lens with a matching name is inside, remove it"""
        to_remove = None
        for existing_lens in self.contents:
            if existing_lens.name == lens_name:
                to_remove = existing_lens
                break
        if to_remove is not None:
            self.contents.remove(to_remove)

    def __str__(self) -> str:
        return f"Box {self.id}: " + " ".join(str(lens) for lens in self.contents)

    def calculate_power(self) -> int:
        """Calculates power of the box by summing powers of the lenses"""
        result = 0
        for slot_number, lens in enumerate(self.contents):
            box_power = 1 + self.id
            slot_power = slot_number + 1
            power = box_power * slot_power * lens.focal_length
            result += power

        return result


def parse_step_pt2(raw_step: str) -> Step:
    """Handles as step in part 2"""
    if len(splits := raw_step.split("=")) == 2:
        box = get_string_hash(splits[0])
        strength = int(splits[1].strip())
        return Step(splits[0], box, strength, AddRemove.Add)
    elif len(splits := raw_step.split("-")) == 2:
        box = get_string_hash(splits[0])
        return Step(splits[0], box, process=AddRemove.Remove)

    raise ValueError(raw_step)


def process_steps_pt2(steps: list[Step]) -> int:
    """Process a list of steps"""
    boxes: list[Box] = [Box(i) for i in range(256)]

    for step in steps:
        if step.process == AddRemove.Remove:
            boxes[step.box].remove_lens(step.lens_name)
        else:
            if step.focal_length is None:
                raise ValueError("focal length should not be None")
            lens = Lens(step.lens_name, step.focal_length)
            boxes[step.box].add_lens(lens)

    return sum(box.calculate_power() for box in boxes)


def main() -> None:
    """main function"""
    chars = get_input()
    raw_steps = chars.split(",")
    # q1
    print(sum(get_string_hash(raw_step) for raw_step in raw_steps))

    # q2
    steps = [parse_step_pt2(raw_step) for raw_step in raw_steps]
    print(process_steps_pt2(steps))


if __name__ == "__main__":
    main()
