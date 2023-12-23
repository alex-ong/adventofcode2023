![lint](https://github.com/alex-ong/adventofcode2023/actions/workflows/lint.yml/badge.svg)

Advent of Code 2023
===

Website: https://adventofcode.com/2023

Setup
===

1. Install python 3.11: `winget install Python.Python.3.11 -i`
1. Install dependencies: `pip install -r requirements.txt`

This installs to your default python, so hopefully it all matches up :)
I couldn't be bothered setting up pipenv for this one.

Running
===
This repository is module based.

To run day1: `python -m day01.day1`

Development
===

Install pre-commit `pre-commit install`

Before each commit, it'll check all the things.
You can also run `pre-commit run --all-files` to run it on all files.

After pushing to `origin`, github will run the lint online just to be sure.


