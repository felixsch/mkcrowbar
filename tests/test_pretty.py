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

    assert out == ' Topic... \n  # a task \n'


def test_note(capsys):

    with pretty.step('Topic', indent=0, interactive=False) as s:
        s.task('a task')
        s.note('a note')

    out, _ = capsys.readouterr()

    assert out == ' Topic... \n  # a task \n    ::  a note \n'

def test_done_interactive(capsys):

    with pretty.step('Topic', indent=0, interactive=True) as s:
        s.task('a task')
        s.done('its done')

    out, _ = capsys.readouterr()

    assert 'its done' in out
