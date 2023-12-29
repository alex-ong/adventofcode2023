"""PipeBounds class."""
from enum import Enum


class PipeBounds(Enum):
    """Whether this tile is a pipe, inside, outside or currently unknown."""

    INSIDE = 0
    OUTSIDE = 1
    UNKNOWN = 2
    PIPE = 3
