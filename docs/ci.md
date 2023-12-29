# Continuous Integration

CI allows lots of processes to occur automatically

Think of `pre-commit` as "local" and `github actions` as cloud.

1. `pre-commit` is a tool that runs arbitrary scripts at `pre-commit` and `pre-push` time. You can reuse it's config for github-action based scripts, to ensure all ci scripts are run.

2. `github actions` (see `.github/workflows`) are workflows that run "on the cloud" on github.com. They run based on a few conditions such as pushing/merging, PRs etc. They mainly just setup an linux box to install `pre-commit` and then duplicate what was being done on a local environment. They also publish our html documentation (such as this page) into the `gh-pages` branch.


## Tools


### Pre-commit

`pre-commit` is both the name of a tool, and of a stage in committing.

This section details what is done at the stages
1. `pre-commit`: runs `ruff-linting` and `mypy` and `mixed-crlf`. These are all very fast and ensure commits have barebones checks before going in.

2. `pre-push`: runs `pytest unit tests` as well as `coverage`

### ruff
A simple tool that does linting

### mypy
Type-checking tool

### mixed-crlf
Ensures that we don't commit any `crlf` files. Converts all to `lf`

### pytest
Unit testing framework

### coverage
`Coverage` is a simple tool that tells you what % of your code is covered by tests. This can be easily gamed, for example a test that is `assert main() == 0` will result in very high coverage but not necessarily good tests.

### sphinx
Generates `.rst` files and `html` files automatically. You can inject markdown manually. Check the [autodoc](autodoc.md) page for more information.