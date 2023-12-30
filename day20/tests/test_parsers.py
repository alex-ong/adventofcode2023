"""Test parsing code."""
from day20.day20 import FILE_A, FILE_B
from day20.lib.classes import (
    BaseModule,
    BroadcastModule,
    ConjunctionModule,
    FlipFlopModule,
)
from day20.lib.parsers import finalize_modules, get_modules, parse_line


def test_parse_line() -> None:
    """Test ``parse_line()``."""
    module: BaseModule = parse_line("broadcaster -> a")
    assert isinstance(module, BroadcastModule)
    module = parse_line("%a -> inv, con")
    assert isinstance(module, FlipFlopModule)
    assert module.outputs == ["inv", "con"]

    module = parse_line("&a -> inv, con")
    assert isinstance(module, ConjunctionModule)
    assert module.outputs == ["inv", "con"]


def test_get_modules() -> None:
    """Test ``get_modules``."""
    modules: list[BaseModule] = get_modules(FILE_A)
    assert len(modules) == 5
    assert modules[0].outputs == ["a", "b", "c"]
    assert modules[1].outputs == ["b"]
    assert modules[2].outputs == ["c"]
    assert modules[3].outputs == ["inv"]
    assert modules[4].outputs == ["a"]

    assert isinstance(modules[0], BroadcastModule)
    assert isinstance(modules[1], FlipFlopModule)
    assert isinstance(modules[2], FlipFlopModule)
    assert isinstance(modules[3], FlipFlopModule)
    assert isinstance(modules[4], ConjunctionModule)


def test_finalize_modules() -> None:
    """Test ``finalize_modules()``."""
    modules: list[BaseModule] = get_modules(FILE_A)
    modules = finalize_modules(modules)

    assert isinstance(modules[4], ConjunctionModule)
    assert set(modules[4].inputs.keys()) == {"c"}

    modules = get_modules(FILE_B)
    modules = finalize_modules(modules)
    assert isinstance(modules[4], ConjunctionModule)
    assert set(modules[4].inputs.keys()) == {"a", "b"}
