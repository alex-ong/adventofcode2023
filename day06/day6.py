import math
from dataclasses import dataclass

INPUT_SMALL = "day06/input-small.txt"
INPUT = "day06/input.txt"


@dataclass
class Race:
    """Simple class representing a race and its record"""

    time: int
    record_distance: int


@dataclass
class RaceStrat:
    """class representing a strategy (charge time + run_time)"""

    charge_time: int
    run_time: int

    @property
    def distance(self) -> int:
        return self.run_time * self.speed

    @property
    def speed(self) -> int:
        return self.charge_time


def read_inputs(path: str) -> list[Race]:
    """disgusting but short i guess"""
    with open(path, "r", encoding="utf8") as file:
        times = [int(item) for item in file.readline().split()[1:]]
        distance = [int(item) for item in file.readline().split()[1:]]
        items = [Race(times[i], distance[i]) for i in range(len(times))]
        return items


def calculate_race(race: Race) -> int:
    """naive calcuation of a race"""
    results: list[RaceStrat] = []
    for i in range(race.time):
        charge_time = i
        run_time = race.time - i
        race_strat = RaceStrat(charge_time, run_time)
        if race_strat.distance > race.record_distance:
            results.append(race_strat)

    return len(results)


"""
    let charge_time = x
    total_time = 42899189
    target_distance = 308117012911467
    remaining_time = total_time - x
    
    This gives the equation
    x * (total_time - x) > target_distance
    This is a quadratic formula
    
    x * (total_time - x) - target_distance = 0
    If you solve this, you get where the graph first beats and last beats the target

    Expand/simplify
    -x^2 + total_time * x - target_distance = 0
    swap sign:
    x^2 - total_time * x + target_distance = 0

    now solve using quadratic fromula
    x_top = total_time +- sqrt((total-time^2)-4*1*target_distance)
            ------------------------------------------------------
    x_bottom =                  2
    Once you solve +-, you get the intercepts. The total solution is the higher number minus the lower
"""


def calculate_constant_time(race: Race) -> int:
    """TL;DR Quadratic formula"""
    x_top = race.time - math.sqrt((race.time * race.time) - 4 * race.record_distance)
    x_neg = x_top / 2

    # start is always x_neg j, end is always race.time - start
    start = math.ceil(x_neg)
    end = math.floor(race.time - start)

    # add one because hypothetically if end == start, then you'd get 0 which is wrong.
    # typical fencepost :)
    return end - start + 1


def part1(races: list[Race]) -> int:
    permutations = 1
    for race in races:
        num_strats = calculate_race(race)
        permutations *= num_strats
    return permutations


def part2(race: Race) -> int:
    return calculate_constant_time(race)


def get_giga_race(races: list[Race]) -> Race:
    giga_time = int("".join([str(race.time) for race in races]))
    giga_distance = int("".join([str(race.record_distance) for race in races]))
    giga_race = Race(giga_time, giga_distance)
    return giga_race


def main() -> None:
    """Solves Day 6"""
    races = read_inputs(INPUT)

    # q1 Dataclasses, brute force lmao
    print(part1(races))

    # q2 Quadratic formula; constant time.
    giga_race = get_giga_race(races)
    print(part2(giga_race))


if __name__ == "__main__":
    main()
