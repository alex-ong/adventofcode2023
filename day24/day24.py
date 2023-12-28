"""day24 solution"""
from typing import Optional

import z3

from day24.lib.classes import Hailstone, Vector2
from day24.lib.parsers import parse_input

INPUT = ("day24/input.txt", Vector2(200000000000000, 400000000000000))
INPUT_SMALL = ("day24/input-small.txt", Vector2(7, 27))


def get_intersection_2d(left: Hailstone, right: Hailstone) -> Optional[Vector2]:
    pos1 = left.position.xy
    dir1 = left.velocity.xy
    pos2 = right.position.xy
    dir2 = right.velocity.xy

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


def part2(hailstones: list[Hailstone]) -> int:
    x, y, z = z3.Reals("x y z")
    vx, vy, vz = z3.Reals("vx vy vz")

    solver = z3.Solver()

    for index, hail in enumerate(hailstones[:3]):
        pos = hail.position
        vel = hail.velocity

        t = z3.Real(f"t{index}")
        solver.add(t >= 0)
        solver.add(x + vx * t == pos.x + vel.x * t)
        solver.add(y + vy * t == pos.y + vel.y * t)
        solver.add(z + vz * t == pos.z + vel.z * t)

    print(solver.check())

    model = solver.model()

    rx, ry, rz = (
        model.eval(x).as_long(),
        model.eval(y).as_long(),
        model.eval(z).as_long(),
    )

    if not isinstance(rx, int):
        raise AssertionError("rx is non-int!")
    if not isinstance(ry, int):
        raise AssertionError("ry is non-int!")
    if not isinstance(rz, int):
        raise AssertionError("rz is non-int!")
    return rx + ry + rz


def main() -> None:
    input_data, valid_range = INPUT

    hailstones: list[Hailstone] = parse_input(input_data)
    print(len(hailstones))
    print(part1(hailstones, valid_range))

    print(part2(hailstones))


if __name__ == "__main__":
    main()
