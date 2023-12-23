"""PipeBounds class"""
from enum import Enum


class PipeBounds(Enum):
    INSIDE = 0
    OUTSIDE = 1
    UNKNOWN = 2
    PIPE = 3
