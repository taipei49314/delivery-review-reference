import errno, pathlib
def test_volume_has_kernel_cap():
    files = []
    try:
        for n in range(128):
            path = pathlib.Path('/work/tmp') / str(n)
            files.append(path)
            path.write_bytes(b'x' * 4 * 1024 * 1024)
    except OSError as e:
        assert e.errno == errno.ENOSPC
    else:
        raise AssertionError('tmpfs exceeded declared cap')
    finally:
        for path in files:
            path.unlink(missing_ok=True)
