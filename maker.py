"""maker of accessory files."""
import os
from pathlib import Path
from typing import Iterable


def touch_days(days: Iterable[int]) -> None:
    """Touches each day, creating /lib and /tests and relevant init files."""
    for day in days:
        os.makedirs(f"day{day:02}/lib", exist_ok=True)
        os.makedirs(f"day{day:02}/tests", exist_ok=True)
        Path(f"day{day:02}/tests/__init__.py").touch()
        Path(f"day{day:02}/__init__.py").touch()
        Path(f"day{day:02}/lib/__init__.py").touch()


if __name__ == "__main__":
    touch_days(range(1, 26))
