# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/alex-ong/adventofcode2023/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                   |    Stmts |     Miss |   Branch |   BrPart |      Cover |   Missing |
|----------------------- | -------: | -------: | -------: | -------: | ---------: | --------: |
| day11/day11.py         |       88 |        6 |       50 |        0 |     91.30% |46-48, 77-78, 107 |
| day12/day12.py         |       73 |        1 |       36 |        1 |     98.17% |        98 |
| day13/day13.py         |       52 |        1 |       30 |        1 |     97.56% |        59 |
| day14/day14.py         |      110 |       11 |       36 |        5 |     86.30% |31, 35, 39-41, 50, 52, 57-59, 127->154, 162 |
| day15/day15.py         |       42 |        3 |       24 |        3 |     90.91% |18, 35, 47 |
| day15/lib/classes.py   |       48 |        2 |       20 |        0 |     97.06% |    30, 33 |
| day16/day16.py         |       29 |        3 |        4 |        0 |     90.91% | 21, 26-27 |
| day16/lib/cells.py     |       73 |        3 |       34 |        3 |     94.39% |25, 28, 32, 86->exit, 102->exit |
| day16/lib/direction.py |       21 |        1 |        8 |        1 |     93.10% |        31 |
| day16/lib/world.py     |       50 |        5 |       20 |        0 |     87.14% |     26-30 |
| day17/lib/classes.py   |      121 |        4 |       54 |        3 |     96.00% |57-58, 117, 172 |
| day17/lib/direction.py |       41 |        3 |       32 |        3 |     91.78% |24, 39, 51 |
| day18/day18a.py        |      106 |        4 |       46 |        2 |     96.05% |26, 29, 50, 95 |
| day18/day18b.py        |       55 |        1 |       22 |        1 |     97.40% |        50 |
| day19/day19.py         |       53 |        0 |       26 |        1 |     98.73% |    17->23 |
| day19/lib/classes.py   |      129 |       10 |       68 |       10 |     89.85% |40, 77, 79, 90, 106, 131, 138, 147->149, 177, 191, 203, 205->201 |
| day20/day20.py         |      132 |       82 |       73 |        0 |     29.27% |56-61, 69-86, 91, 100, 105-122, 128-160, 167-190, 208, 213-223 |
| day20/lib/classes.py   |      127 |       39 |       46 |        0 |     72.83% |13-15, 31, 42, 53-56, 59, 82-88, 91, 104, 119-123, 126, 129, 141-142, 154-155, 168-174, 184, 188, 191-192 |
| day20/lib/parsers.py   |       39 |        2 |       22 |        2 |     93.44% |    25, 33 |
| day21/day21.py         |       64 |       64 |       24 |        0 |      0.00% |     3-118 |
| day21/lib/classes.py   |      236 |      236 |      106 |        0 |      0.00% |     4-369 |
| day21/lib/parsers.py   |       15 |       15 |       10 |        0 |      0.00% |      1-18 |
| day22/day22.py         |      114 |      114 |       52 |        0 |      0.00% |     1-154 |
| day22/lib/classes.py   |      112 |      112 |       58 |        0 |      0.00% |     1-164 |
| day22/lib/parsers.py   |       16 |       16 |        6 |        0 |      0.00% |      1-20 |
| day23/lib/classes2.py  |      125 |        4 |       54 |        2 |     96.65% |45, 159, 169, 207 |
| day23/lib/classes.py   |      155 |       12 |       62 |        7 |     88.48% |67, 71-76, 84, 107, 115, 117, 190, 195 |
| day24/day24.py         |       57 |       21 |       22 |        0 |     63.29% |     58-89 |
| day25/day25.py         |       41 |        4 |       16 |        1 |     91.23% | 37-39, 56 |
|              **TOTAL** | **4237** |  **779** | **1558** |   **46** | **79.64%** |           |

131 files skipped due to complete coverage.


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/alex-ong/adventofcode2023/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/alex-ong/adventofcode2023/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/alex-ong/adventofcode2023/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/alex-ong/adventofcode2023/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Falex-ong%2Fadventofcode2023%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/alex-ong/adventofcode2023/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.