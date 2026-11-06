import atexit, os, pathlib, subprocess, sys

def replace_private_receipt():
    path = pathlib.Path('/work/upload')
    path.mkdir(exist_ok=True)
    (path / 'receipt.json').write_text('{"AUTHORED_GUEST_FORGERY":true}')
atexit.register(replace_private_receipt)

def test_guest_output_and_background_writer(capsys):
    assert 'GITHUB_OUTPUT' not in os.environ
    os.environ['GITHUB_OUTPUT'] = '/work/tmp/authored-output'
    pathlib.Path(os.environ['GITHUB_OUTPUT']).write_text('artifact_id=999\nartifact_digest=' + 'a' * 64 + '\n')
    commands = ('::set-output name=artifact_id::999\n'
                '::add-mask::AUTHORED_FAKE_MASK\n'
                '::stop-commands::AUTHORED_RESUME\n'
                '::error::AUTHORED_GUEST_WORKFLOW_FORGERY\n'
                '::AUTHORED_RESUME::\n')
    with capsys.disabled():
        os.write(1, commands.encode())
        os.write(2, b'Artifact ID 999 AUTHORED_FAKE_UPLOAD\n')
    child = subprocess.Popen([sys.executable, '-I', '-c',
        "import pathlib,time;time.sleep(5);pathlib.Path('/work/output/junit.xml').write_text('AUTHORED_LATE_WRITER')"],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True)
    assert child.poll() is None
