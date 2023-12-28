from day20.lib.classes import BroadcastModule, LoopCounter, Pulse, SinkModule


def test_modules() -> None:
    """Ensure that sink/broadcast module are always in default state"""
    sink: SinkModule = SinkModule("rx", [])
    assert sink.is_default_state()
    broadcast: BroadcastModule = BroadcastModule("broadcast", ["sink"])
    assert broadcast.is_default_state()
    broadcast.handle_pulse("button", Pulse.LOW)
    assert broadcast.is_default_state()
    sink.handle_pulse("broadcast", Pulse.LOW)
    assert sink.is_default_state()


def test_loop_counter() -> None:
    loop_counter: LoopCounter = LoopCounter(4)
    loop_counter.add_result("loop1", 4)
    loop_counter.add_result("loop1", 6)
    loop_counter.add_result("loop1", 8)
    assert not loop_counter.finished
    loop_counter.add_result("loop2", 9)
    assert not loop_counter.finished
    loop_counter.add_result("loop3", 10)
    assert not loop_counter.finished
    loop_counter.add_result("loop4", 15)
    assert loop_counter.finished
    assert loop_counter.loop_lengths == {
        "loop1": 4,
        "loop2": 9,
        "loop3": 10,
        "loop4": 15,
    }
