"""Parse vectors/boxes from string to class."""
from day22.lib.classes import BoxData, Vector3


def parse_vector(string: str) -> Vector3:
    """Returns a wellformed vector from a string.

    e.g. 1,2,3
    """
    x, y, z = string.split(",")
    return Vector3(int(x), int(y), int(z))


def get_boxes(path: str) -> list[BoxData]:
    """Returns a wellformed box from a string.

    E.g. 1,2,3~1,2,4
    """
    boxes: list[BoxData] = []
    with open(path, encoding="utf8") as file:
        for index, line in enumerate(file):
            line = line.strip()
            vec1, vec2 = line.split("~")
            from_vec = parse_vector(vec1)
            to_vec = parse_vector(vec2)
            boxes.append(BoxData(str(index), from_vec, to_vec))
    return boxes
