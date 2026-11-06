"""Authored fixed UTC failure window, identical on BASE and HEAD."""
import time

WINDOW_START_UTC_EPOCH = 1793955483
WINDOW_END_UTC_EPOCH = 1793956113

def test_fixed_failure_window():
    observed = time.time()
    assert not (WINDOW_START_UTC_EPOCH <= observed <= WINDOW_END_UTC_EPOCH), "authored failure window"
