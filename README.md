[![lint](https://github.com/alex-ong/adventofcode2023/actions/workflows/lint.yml/badge.svg)](https://github.com/alex-ong/adventofcode2023/actions/workflows/lint.yml)
[![test](https://github.com/alex-ong/adventofcode2023/actions/workflows/test.yml/badge.svg)](https://github.com/alex-ong/adventofcode2023/actions/workflows/test.yml)
[![coverage](https://raw.githubusercontent.com/alex-ong/adventofcode2023/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/alex-ong/adventofcode2023/blob/python-coverage-comment-action-data/htmlcov/index.html)

Advent of Code 2023
===

Website: https://adventofcode.com/2023

API documentation and more information:

https://alex-ong.github.io/adventofcode2023/index.html


Setup
===

1. Install python 3.11: `winget install Python.Python.3.11 -i`
1. Install dependencies: `pip install -r requirements.txt`
1. Install Graphviz for all users: `winget install Graphviz.Graphviz -i ` 

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


