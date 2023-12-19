import os
import time

import dotenv
import requests

BASE_URL = "https://adventofcode.com/2023/day/{}/input"


def main() -> None:
    dotenv.load_dotenv()
    session = os.environ.get("SESSION", None)
    if session is None:
        print("Enter session (https://adventofcode.com/2023/day/1/input)")
        print("then F12, networking, refresh, cookies:")
        session = input()
        if session.startswith("session="):
            session = session[len("session=") :]
    print("using session:", session)

    # grab last day
    subfolders: list[str] = [
        f.name for f in os.scandir(".") if f.is_dir() and f.name.startswith("day")
    ]

    last_day_name: str = max(subfolders)
    last_day: int = int(last_day_name[3:])

    for day in range(1, last_day + 1):
        download_file(day, session)


def download_file(day: int, session: str) -> None:
    output_path = os.path.join(f"day{day:02d}", "input.txt")
    if os.path.exists(output_path):
        print("No download; file already exists")
        return

    # Create the subdirectory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Download the file
    url = BASE_URL.format(day)
    response = requests.get(url, cookies={"session": session})
    time.sleep(1)  # don't spam the guys server, ok
    if response.status_code == 200:
        with open(output_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {url} to {output_path}")
    else:
        print(f"Failed to download {url} (Status code: {response.status_code})")


if __name__ == "__main__":
    main()
