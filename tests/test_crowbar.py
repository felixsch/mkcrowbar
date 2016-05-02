from mkcrowbar import crowbar

from fake import LocalCommands, has_args, return_ok, raise_error

validator = '/opt/dell/bin/network-json-validator'


def test_network_config_valid(monkeypatch):

    local = LocalCommands()
    monkeypatch.setattr('mkcrowbar.crowbar.local', local)
    monkeypatch.setattr('os.path.exists', lambda x: True)

    # everything is normal
    local.has(validator, has_args(['--admin-ip'], return_ok()))
    (code, _, _) = crowbar.network_config_valid('127.0.0.1')
    assert code is 0

    # network-json-validator does not exist
    local.has(validator, raise_error(FileNotFoundError('stub')))
    ret = crowbar.network_config_valid('127.0.0.1')
    assert ret is None
