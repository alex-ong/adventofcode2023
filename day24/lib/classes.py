"""Day24 classes."""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Vector3:
    """Simple 3d vector."""

    x: float
    y: float
    z: float

    @property
    def xy(self) -> "Vector2":
        """Convert to vector2."""
        return Vector2(self.x, self.y)


@dataclass(frozen=True, slots=True)
class Vector2:
    """Simple vector2."""

    x: float
    y: float


@dataclass(frozen=True)
class Hailstone:
    """Hailstone has a 3d vector for pos/velocity."""

    position: Vector3
    velocity: Vector3
