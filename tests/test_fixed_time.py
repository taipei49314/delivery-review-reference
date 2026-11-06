"""Authored fixed UTC cutoff control, identical on BASE and HEAD."""
import time

CUTOFF_UTC_EPOCH = 1793955813

def test_fixed_cutoff():
    assert time.time() < CUTOFF_UTC_EPOCH, "authored cutoff reached"
