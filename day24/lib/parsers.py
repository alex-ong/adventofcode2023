from day24.lib.classes import Hailstone, Vector3


def parse_vector3(line: str) -> Vector3:
    line = line.strip()
    x, y, z = line.split(",")
    return Vector3(int(x), int(y), int(z))


def parse_input(filename: str) -> list[Hailstone]:
    result: list[Hailstone] = []
    with open(filename, "r", encoding="utf8") as file:
        for line in file:
            line = line.strip()
            left, right = line.split("@")
            pos, velocity = parse_vector3(left), parse_vector3(right)
            result.append(Hailstone(pos, velocity))
    return result
