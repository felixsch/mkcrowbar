from mkcrowbar import crowbar

import fake

def test_network_config_valid(monkeypatch):

    local = fake.LocalCommands()
    monkeypatch.setattr('mkcrowbar.crowbar.local', local)
    monkeypatch.setattr('os.path.exists', lambda x: True)

    def has_admin_ip(*args):
        if "--admin-ip" not in args:
            raise RuntimeError('Could not find admin-ip argument.')

    # everything is normal
    local.has('/opt/dell/bin/network-json-validator', fake.returnOk(expect=has_admin_ip))
    (code, _, _) = crowbar.network_config_valid('127.0.0.1')

    assert code is 0


    # network-json-validator does not exist

    local.has('/opt/dell/bin/network-json-validator', fake.raiseError(FileNotFoundError('stub')))
    
    ret = crowbar.network_config_valid('127.0.0.1')

    assert ret is None
