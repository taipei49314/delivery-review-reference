from billing import compute_total

def test_total():
    assert compute_total([1, 2]) > 0
