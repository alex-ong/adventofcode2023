from lib.classes import BoxData, Vector3


def parse_vector(string: str) -> Vector3:
    x, y, z = string.split(",")
    return Vector3(int(x), int(y), int(z))


def get_boxes() -> list[BoxData]:
    boxes: list[BoxData] = []
    with open("input.txt", encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if len(line) == 0:
                break
            vec1, vec2 = line.split("~")
            from_vec = parse_vector(vec1)
            to_vec = parse_vector(vec2)
            boxes.append(BoxData(from_vec, to_vec))
    return boxes
