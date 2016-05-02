import sys
from unittest import mock
from mkcrowbar import crowbar
import fake

@mock.patch('plumbum.local', "fooobbbabababa")
@mock.patch('plumbum.machines.local', "fooobbbabababa")
@mock.patch('plumbum.machines.local', fake.LocalModule())
def test_network_config_valid(monkeypatch):



    # chef templates exists
    # monkeypatch.setattr('os.path.exists', lambda _: True)


    monkeypatch.setattr('plumbum.machines.local', fake.LocalModule())
    sys.modules['plumbum.machines.local'] = "WAAAAAA"








    ret = crowbar.network_config_valid('127.0.0.1')

    assert ret is True

    # chef templates do not exits
    pass
