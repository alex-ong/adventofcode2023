"""Functions to parse from a file into well defined classes."""
from day03.lib.classes import Matrix


def get_matrix(path: str) -> Matrix:
    """Convert text file to matrix."""
    with open(path, "r", encoding="utf8") as file:
        data = file.readlines()
        data = [line.strip() for line in data]
    return Matrix(data=data)
