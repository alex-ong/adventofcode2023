"""day1a solution"""


def main():
    with open("test.txt", "r", encoding="utf8") as file:
        total = 0
        for line in file:
            first = None
            last = None
            for char in line:
                if char.isnumeric():
                    if first is None:
                        first = char
                    last = char
            print(line.strip())
            data = int(first + last)

            total += data
        print(total)


if __name__ == "__main__":
    main()
