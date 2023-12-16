"""day1a solution"""


def main():
    with open("test.txt", "r", encoding="utf8") as file:
        total = 0
        for line in file:
            first: str | None = None
            last: str
            for char in line:
                if char.isnumeric():
                    if first is None:
                        first = char
                    last = char

            if first is None:
                raise ValueError("first should be set by now")
            data = int(first + last)

            total += data
        print(total)


if __name__ == "__main__":
    main()
