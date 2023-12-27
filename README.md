# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/alex-ong/adventofcode2023/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                  |    Stmts |     Miss |   Branch |   BrPart |      Cover |   Missing |
|---------------------- | -------: | -------: | -------: | -------: | ---------: | --------: |
| day19/day19.py        |       53 |        0 |       26 |        1 |     98.73% |    17->23 |
| day19/lib/classes.py  |      129 |       10 |       68 |       10 |     89.85% |40, 77, 79, 90, 106, 131, 138, 147->149, 177, 191, 203, 205->201 |
| day20/day20.py        |      132 |       82 |       73 |        0 |     29.27% |56-61, 69-86, 91, 100, 105-122, 128-160, 167-190, 208, 213-223 |
| day20/lib/classes.py  |      127 |       39 |       46 |        0 |     72.83% |13-15, 31, 42, 53-56, 59, 82-88, 91, 104, 119-123, 126, 129, 141-142, 154-155, 168-174, 184, 188, 191-192 |
| day20/lib/parsers.py  |       39 |        2 |       22 |        2 |     93.44% |    25, 33 |
| day21/day21.py        |       64 |       64 |       24 |        0 |      0.00% |     3-118 |
| day21/lib/classes.py  |      236 |      236 |      106 |        0 |      0.00% |     4-369 |
| day21/lib/parsers.py  |       15 |       15 |       10 |        0 |      0.00% |      1-18 |
| day22/day22.py        |      114 |      114 |       52 |        0 |      0.00% |     1-154 |
| day22/lib/classes.py  |      112 |      112 |       58 |        0 |      0.00% |     1-164 |
| day22/lib/parsers.py  |       16 |       16 |        6 |        0 |      0.00% |      1-20 |
| day23/lib/classes2.py |      125 |        1 |       54 |        0 |     99.44% |        45 |
| day23/lib/classes.py  |      155 |       12 |       62 |        7 |     88.48% |67, 71-76, 84, 107, 115, 117, 190, 195 |
| day24/day24.py        |       57 |       21 |       22 |        0 |     63.29% |     58-89 |
| day25/day25.py        |       41 |        4 |       16 |        1 |     91.23% | 37-39, 56 |
|             **TOTAL** | **4240** |  **728** | **1524** |   **21** | **81.09%** |           |

146 files skipped due to complete coverage.


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