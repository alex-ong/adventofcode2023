"""Test day25 main functions."""
from day25.day25 import INPUT_SMALL, Connection, get_data, parse_connection, solve_nodes


def test_get_data() -> None:
    """Test ``get_data()``."""
    conns: list[Connection] = get_data(INPUT_SMALL)
    assert len(conns) == 13
    assert conns[0].src == "jqt"


def test_parse_connection() -> None:
    """Test ``parse_connection()``."""
    conn: Connection = parse_connection("zmx: vfl mgb tmr bsn")
    assert conn.src == "zmx"
    assert set(conn.dests) == {"vfl", "mgb", "tmr", "bsn"}


def test_day25() -> None:
    """Test ``solve_nodes()``."""
    conns: list[Connection] = get_data(INPUT_SMALL)
    assert solve_nodes(conns) == 54
