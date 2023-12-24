"""day24 solution"""
from typing import Optional

from day24.lib.classes import Hailstone, Vector2
from day24.lib.parsers import parse_input

INPUT = ("day24/input.txt", Vector2(200000000000000, 400000000000000))
INPUT_SMALL = ("day24/input-small.txt", Vector2(7, 27))


def get_intersection_2d(left: Hailstone, right: Hailstone) -> Optional[Vector2]:
    pos1 = left.position.xy
    dir1 = left.trajectory.xy
    pos2 = right.position.xy
    dir2 = right.trajectory.xy

    determinant = (dir1.x * dir2.y) - (dir1.y * dir2.x)

    if determinant == 0:
        return None  # parallel

    t1 = ((pos2.x - pos1.x) * dir2.y - (pos2.y - pos1.y) * dir2.x) / determinant
    t2 = ((pos2.x - pos1.x) * dir1.y - (pos2.y - pos1.y) * dir1.x) / determinant

    if t1 < 0:  # in the past :(
        return None
    if t2 < 0:  # in the past :(
        return None
    intersection_point = Vector2(pos1.x + t1 * dir1.x, pos1.y + t1 * dir1.y)
    return intersection_point


def within_2d(point: Vector2, min_max: Vector2) -> bool:
    return min_max.x <= point.x <= min_max.y and min_max.x <= point.y <= min_max.y


def part1(hailstones: list[Hailstone], valid_range: Vector2) -> int:
    result = 0
    print(len(hailstones))
    left: Hailstone
    right: Hailstone
    for index, left in enumerate(hailstones[:-1]):
        for right in hailstones[index + 1 :]:
            intersection: Optional[Vector2] = get_intersection_2d(left, right)

            if intersection is None:
                continue

            if within_2d(intersection, valid_range):
                result += 1

    return result


def main() -> None:
    input_data, valid_range = INPUT

    hailstones: list[Hailstone] = parse_input(input_data)
    print(len(hailstones))
    print(part1(hailstones, valid_range))


if __name__ == "__main__":
    main()
