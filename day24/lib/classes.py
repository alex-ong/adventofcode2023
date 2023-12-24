from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Vector3:
    x: float
    y: float
    z: float

    @property
    def xy(self) -> "Vector2":
        return Vector2(self.x, self.y)


@dataclass(frozen=True, slots=True)
class Vector2:
    x: float
    y: float


@dataclass(frozen=True)
class Hailstone:
    position: Vector3
    trajectory: Vector3
