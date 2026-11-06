import os
def test_authored_output_limit(capsys):
    with capsys.disabled():
        os.write(1, b'x' * 2000000)
