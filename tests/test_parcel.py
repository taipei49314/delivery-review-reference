import pytest

def test_authored_pass():
    assert 2 + 2 == 4

@pytest.mark.skip(reason='authored permitted partial skip')
def test_authored_skip():
    assert 2 + 2 == 4
