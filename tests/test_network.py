from mkcrowbar import network

from fake import LocalCommands, LocalCommand, has_args, load_fixture


def test_iface_has_ipv4_addr(capsys, monkeypatch):
    local = LocalCommands()
    monkeypatch.setattr('mkcrowbar.network.local', local)

    args = ['-f', 'inet', 'addr', 'show', 'eth0']

    local.has('ip', has_args(args, load_fixture('ip_addr_show')))

    ip = network.iface_has_ipv4_addr('eth0')
    assert ip == '11.22.33.44'


def test_iface_backup_configuration(monkeypatch):
    iface = 'eth0'
    home_path = '/root/.mkcrowbar'
    iface_path = '/etc/sysconfig/network/ifcfg-' + iface

    monkeypatch.setattr('os.path.exists', LocalCommand('path.exists', has_args([home_path], True)))
    monkeypatch.setattr('os.makedirs', LocalCommand('makedirs', has_args([home_path])))
    monkeypatch.setattr('os.path.isfile', LocalCommand('path.isfile', has_args([iface_path])))
    monkeypatch.setattr('os.rename', LocalCommand('rename', has_args([iface_path])))

    network.iface_backup_configuration(iface)


class StubOpen():
    """
    Fake a file handle
    """
    def __init__(self):
        self.content = []

    def write(self, line):
        self.content += [line]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def result(self):
        return self.content


def test_set_static_addr(monkeypatch):
    iface = 'eth0'
    path  = '/etc/sysconfig/network/ifcfg-' + iface
    stub_file = StubOpen()

    monkeypatch.setattr('mkcrowbar.network.iface_backup_configuration',
                        LocalCommand('backup', has_args([iface])))


    monkeypatch.setattr('builtins.open',  LocalCommand('open', has_args([path], lambda *args: stub_file)))

    network.iface_set_static_addr(iface, {'FOO': 'bar'})

    assert 'DEVICE=eth0\n' in stub_file.result()
    assert 'BOOTPROTO=static\n' in stub_file.result()
    assert 'FOO=bar\n' in stub_file.result()







def test_stop(monkeypatch):
    pass


def test_start(monkeypatch):
    pass


def test_uses_dhcp(monkeypatch):
    pass


def test_hostname(monkeypatch):
    pass


def test_is_qualified_hostname(monkeypatch):
    pass


def test_add_to_hosts(monkeypatch):
    pass
