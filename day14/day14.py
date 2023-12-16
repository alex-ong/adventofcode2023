"""day14 solution"""


def get_input():
    with open("input.txt") as file:
        world = list(file)

    return list(zip(*world))  # rotate 90 degrees


def calculate_row(row):
    """Calculates the value after one iteration"""
    square_indices = [-1] + [i for i, x in enumerate(row) if x == "#"] + [len(row)]
    pairs = zip(square_indices, square_indices[1:])
    row_score = 0
    for start, end in pairs:
        sub_array = row[start + 1 : end]
        o_count = sub_array.count("O")
        start_score = len(row) - (start + 1)
        end_score = len(row) - start - o_count
        sub_array_score = (start_score + end_score) / 2 * o_count
        row_score += sub_array_score
    return row_score


def main():
    world = get_input()
    # world is rotated 90 degrees,
    # so we just need to sum rows instead of cols
    # q1:
    print(sum(calculate_row(row) for row in world))


if __name__ == "__main__":
    main()
