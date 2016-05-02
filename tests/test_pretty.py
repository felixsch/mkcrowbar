from pytest import raises

from mkcrowbar import pretty


def test_say(capsys):
    pretty.say('foo')

    out, _ = capsys.readouterr()

    assert out == 'foo\n'


def test_fatal(capsys):

    pretty.fatal('fatal', exit=None)

    _, err = capsys.readouterr()
    assert err == '  Fatal: fatal\n'

    with raises(SystemExit):
        pretty.fatal('fatal2', exit=17)

        _, err = capsys.readouterr()
        assert err == '  Fatal: fatal2\n'


def test_warn(capsys):
    pretty.warn('a warning')

    _, err = capsys.readouterr()

    assert err == '  Warning: a warning\n'


def test_info(capsys):
    pretty.info('a information')

    out, _ = capsys.readouterr()

    assert out == '  Info: a information\n'


def test_step_task_interactive(capsys):

    with pretty.step('Topic', indent=0, interactive=True) as s:
        s.task('a task')

    out, _ = capsys.readouterr()

    assert 'Topic...' in out
    assert '✓ a task' in out


def test_step_task(capsys):


    with pretty.step('Topic', indent=0, interactive=False) as s:
        s.task('a task')

    out, _ = capsys.readouterr()

    assert 'Topic...' in out
    assert '# a task' in out
    assert '✓ a task' in out


def test_note(capsys):

    with pretty.step('Topic', indent=0, interactive=False) as s:
        s.task('a task')
        s.note('a note')

    out, _ = capsys.readouterr()

    assert 'Topic...' in out
    assert '# a task' in out
    assert '✓ a task' in out
    assert 'a note' in out

def test_done(capsys):
    with pretty.step('Topic', indent=0) as s:
        s.task('a task')
        s.done('its done')

    out, _ = capsys.readouterr()

    assert 'Topic...' in out
    assert '# a task' in out
    assert '✓ a task [its done]' in out

def test_fail(capsys):

    with raises(SystemExit):
        with pretty.step('Topic', indent=0) as s:
            s.task('a task')
            s.fail('failed')

    out, err = capsys.readouterr()

    assert 'Topic...' in out
    assert '# a task' in out
    assert '==> failed' in err


def test_success(capsys):

    with pretty.step('Topic', indent=0) as s:
        s.task('a task')
        s.success('success')

    out, _ = capsys.readouterr()

    assert 'Topic...' in out
    assert '# a task' in out
    assert '==> success' in out
