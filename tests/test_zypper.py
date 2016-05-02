from functools import partial
from mkcrowbar import zypper

import fake


def stub_cmd(expected, *args):
    for expect in expected:
        if expect not in args:
            raise RuntimeError("""
                               zypper.cmd called without `{arg}`...
                               Call was: zypper {commands}
                               """.format(arg=expect, commands=" ".join(args)))
    return fake.LocalCommand('zypper', fake.returnOk())


def test_cmd(monkeypatch):
    local = fake.LocalCommands()
    monkeypatch.setattr('mkcrowbar.zypper.local', local)

    def non_interactive_args(*args):
        if '--non-interactive' not in args or '--no-gpg-checks' not in args:
            raise RuntimeError('Missing args: --non-interactive or --no-gpg-checks')

    local.has('zypper', fake.returnOk(expect=non_interactive_args))

    update = zypper.cmd('update')

    (code, _, _) = update.run(retcode=0)

    assert code is 0


def test_repo_exists(monkeypatch):
    ret = zypper.repo_exists('http://download.opensuse.org/tumbleweed/repo/oss/')
    assert ret is True

    ret = zypper.repo_exists('http://download.opensuse.org/xxxxxxxxxxxxxxxxxxxxxxxx/')
    assert ret is False

    ret = zypper.repo_exists('asidjsad')
    assert ret is False


def test_repo_enable(monkeypatch):
    repo_url = 'http://download.opensuse.org/tumbleweed/repo/oss/'
    repo_alias = 'tumbleweed-oss'

    repo_repo = 'http://..../openSUSE_Tumbleweed/devel:languages:python3.repo'

    # simple call
    monkeypatch.setattr('mkcrowbar.zypper.cmd', partial(stub_cmd, [repo_repo]))
    (code, _, _) = zypper.repo_enable(repo_repo)
    assert code is 0

    # url / alias call
    monkeypatch.setattr('mkcrowbar.zypper.cmd', partial(stub_cmd, ['ar', repo_url, repo_alias]))
    (code, _, _) = zypper.repo_enable(repo_url, repo_alias)
    assert code is 0

    # with settings
    monkeypatch.setattr('mkcrowbar.zypper.cmd', partial(stub_cmd, ['ar', repo_repo, '--some-settings']))
    (code, _, _) = zypper.repo_enable(repo_repo, settings={'some-settings': 'foo'})
    assert code is 0


def test_refresh(monkeypatch):
    monkeypatch.setattr('mkcrowbar.zypper.cmd', partial(stub_cmd, ['ref']))
    (code, _, _) = zypper.refresh()
    assert code is 0


def test_install(monkeypatch):
    monkeypatch.setattr('mkcrowbar.zypper.cmd', partial(stub_cmd, ['in', 'foo']))
    (code, _, _) = zypper.install(['foo'])
    assert code is 0


def test_remove(monkeypatch):
    monkeypatch.setattr('mkcrowbar.zypper.cmd', partial(stub_cmd, ['rm', 'foo']))
    (code, _, _) = zypper.remove(['foo'])
    assert code is 0


























