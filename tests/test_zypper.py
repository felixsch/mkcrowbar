from functools import partial
from mkcrowbar import zypper

from fake import LocalCommand, LocalCommands, has_args, return_ok


def stub_cmd(required, *args):
    cmd = LocalCommand('zypper', has_args(required, return_ok()))
    cmd[args]
    return cmd


def test_cmd(monkeypatch):
    local = LocalCommands()
    monkeypatch.setattr('mkcrowbar.zypper.local', local)

    args = ['--non-interactive', '--no-gpg-checks']

    local.has('zypper', has_args(args, return_ok()))

    update = zypper.cmd('update')

    (code, _, _) = update.run(retcode=0)

    assert code is 0


def test_repo_exists():
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
