import os, pathlib, socket, errno, ctypes
def test_boundary():
    assert os.getuid() == 65532
    assert not any(k.startswith(('GH_', 'GITHUB_', 'ACTIONS_', 'DOCKER_')) for k in os.environ)
    assert not pathlib.Path('/var/run/docker.sock').exists()
    for p in ('/source/attempt.txt', '/trusted/attempt.txt', '/wheels/attempt.txt', '/etc/attempt.txt'):
        try:
            pathlib.Path(p).write_text('forbidden')
        except OSError as e:
            assert e.errno in (errno.EROFS, errno.EACCES)
        else:
            raise AssertionError('writable outside private tmpfs')
    with socket.socket() as s:
        s.settimeout(.2)
        assert s.connect_ex(('1.1.1.1', 443)) != 0
    status = pathlib.Path('/proc/self/status').read_text()
    assert status.split('NoNewPrivs:')[1].splitlines()[0].strip() == '1'
    assert status.split('CapEff:')[1].splitlines()[0].strip() == '0000000000000000'
    assert status.split('Seccomp:')[1].splitlines()[0].strip() == '2'
    # Linux amd64 io_uring_setup is intentionally absent from the pinned allowlist.
    # Invalid pointers cannot be reached: the syscall must be rejected with EPERM.
    libc = ctypes.CDLL(None, use_errno=True)
    assert libc.syscall(425, 0, 0) == -1 and ctypes.get_errno() == errno.EPERM
    assert pathlib.Path('/sys/fs/cgroup/memory.max').read_text().strip() == '536870912'
    assert pathlib.Path('/sys/fs/cgroup/pids.max').read_text().strip() == '64'
    assert pathlib.Path('/sys/fs/cgroup/cpu.max').read_text().strip() == '100000 100000'
    stats = os.statvfs('/work')
    assert stats.f_blocks * stats.f_frsize == 256 * 1024 * 1024

def test_exact_pinned_runtime():
    import sys, platform
    assert sys.version_info[:3] == (3, 11, 16)
    assert sys.implementation.name == 'cpython'
    assert sys.platform == 'linux'
    assert platform.machine() == 'x86_64'

def test_host_files_and_workflow_command_files_are_unavailable():
    import os, pathlib
    for name in ('GITHUB_ENV', 'GITHUB_OUTPUT', 'GITHUB_PATH', 'GITHUB_STATE',
                 'GITHUB_STEP_SUMMARY', 'ACTIONS_ID_TOKEN_REQUEST_URL',
                 'ACTIONS_ID_TOKEN_REQUEST_TOKEN', 'ACTIONS_RUNTIME_TOKEN'):
        assert name not in os.environ
    for value in ('/home/runner/work', '/home/runner/.config/gh/hosts.yml',
                  '/root/.config/gh/hosts.yml', '/var/run/docker.sock'):
        try:
            pathlib.Path(value).read_bytes()
        except (PermissionError, FileNotFoundError, IsADirectoryError):
            pass
        else:
            raise AssertionError('host path unexpectedly readable')
