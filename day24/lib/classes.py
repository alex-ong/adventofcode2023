from dataclasses import dataclass


@dataclass(frozen=True)
class Vector3:
    x: int
    y: int
    z: int


@dataclass(frozen=True)
class Hailstone:
    position: Vector3
    trajectory: Vector3
