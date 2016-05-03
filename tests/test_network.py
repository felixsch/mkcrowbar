from pytest import raises
from mkcrowbar import network

from fake import *


def test_iface_has_ipv4_addr(capsys, monkeypatch):
    local = LocalCommands()
    monkeypatch.setattr('mkcrowbar.network.local', local)

    args = ['-f', 'inet', 'addr', 'show', 'eth0']

    local.has('ip', expect_args(args, load_fixture('ip_addr_show')))

    ip = network.iface_has_ipv4_addr('eth0')
    assert ip == '11.22.33.44'


def test_iface_backup_configuration(monkeypatch):
    iface = 'eth0'
    home_path = '/root/.mkcrowbar'
    iface_path = '/etc/sysconfig/network/ifcfg-' + iface

    monkeypatch.setattr('os.path.exists', LocalCommand('path.exists', expect_args([home_path], True)))
    monkeypatch.setattr('os.makedirs', LocalCommand('makedirs', expect_args([home_path])))
    monkeypatch.setattr('os.path.isfile', LocalCommand('path.isfile', expect_args([iface_path])))
    monkeypatch.setattr('os.rename', LocalCommand('rename', expect_args([iface_path])))

    network.iface_backup_configuration(iface)



def test_set_static_addr(monkeypatch):
    iface = 'eth0'
    path  = '/etc/sysconfig/network/ifcfg-' + iface
    stub_file = StubOpen()

    monkeypatch.setattr('mkcrowbar.network.iface_backup_configuration',
                        LocalCommand('backup', expect_args([iface])))


    monkeypatch.setattr('builtins.open',  LocalCommand('open', expect_args([path], lambda *args: stub_file)))

    network.iface_set_static_addr(iface, {'FOO': 'bar'})

    assert 'DEVICE=eth0\n' in stub_file.result()
    assert 'BOOTPROTO=static\n' in stub_file.result()
    assert 'FOO=bar\n' in stub_file.result()


def test_start_stop(monkeypatch):
    iface = 'eth1'
    local = LocalCommands()
    monkeypatch.setattr('mkcrowbar.network.local', local)

    local.has('ifdown', expect_args([iface], return_ok()))
    assert network.iface_stop(iface) is True

    local.has('ifdown', expect_args([iface], return_error()))
    assert network.iface_stop(iface) is False

    local.has('ifup', expect_args([iface], return_ok()))
    assert network.iface_start(iface) is True

    local.has('ifup', expect_args([iface], return_error()))
    assert network.iface_start(iface) is False

def test_uses_dhcp(monkeypatch):
    iface = 'eth1'
    path = '/etc/sysconfig/network/ifcfg-' + iface
    dhcp = StubOpen(monkeypatch, expect_args([path], load_fixture('ifcfg-dhcp')))
    static = StubOpen(monkeypatch, expect_args([path], load_fixture('ifcfg-static')))


    monkeypatch.setattr('builtins.open', lambda *args: dhcp(args))
    assert network.iface_uses_dhcp(iface) is True

    monkeypatch.setattr('builtins.open', lambda *args: static(args))
    assert network.iface_uses_dhcp(iface) is False


def test_hostname(capsys, monkeypatch):
    local = LocalCommands()
    monkeypatch.setattr('mkcrowbar.network.local', local)

    local.has('hostname', expect_args(['-f'], return_ok('  test.testme.com  ')))
    assert network.hostname('-f') == 'test.testme.com'

    local.has('hostname', expect_args(['-f'], return_error('hostname: Name or service not known')))
    with raises(SystemExit):

        network.hostname('-f')

        _, err = capsys.readouterr()
        assert err == 'hostname: Name or service not known'


def test_set_hostname(monkeypatch):
    local = LocalCommands()
    monkeypatch.setattr('mkcrowbar.network.local', local)

    local.has('hostname', expect_args(['newhostname'], return_ok()))
    assert network.set_hostname('newhostname') is True


def test_is_qualified_hostname(monkeypatch):

    assert network.is_qualified_hostname('host') is False
    assert network.is_qualified_hostname('moep@floep.com') is False
    assert network.is_qualified_hostname('local.suse.com') is True
    assert network.is_qualified_hostname('superlocal.local.suse.com') is True


def test_add_to_hosts(monkeypatch):
    fqdn = 'example.test.com'
    ip = '192.168.2.111'
    path = '/etc/hosts'
    clean_hosts = StubOpen(monkeypatch, expect_args([path], load_fixture('hosts')))
    added_hosts = StubOpen(monkeypatch, expect_args([path], load_fixture('hosts-already-added')))

    monkeypatch.setattr('builtins.open', lambda *args: clean_hosts(args))
    assert network.add_to_hosts(ip, fqdn) is 0
    assert '192.168.2.111 example.test.com example\n' in clean_hosts.result()

    monkeypatch.setattr('builtins.open', lambda *args: added_hosts(args))
    assert network.add_to_hosts(ip, fqdn) is -1


def test_has_running_firewall(monkeypatch):
    local = LocalCommands()
    monkeypatch.setattr('mkcrowbar.network.local', local)

    local.has('iptables', expect_args(['-S'], "-P INPUT ACCEPT\n-P FORWARD ACCEPT\n-P OUTPUT ACCEPT"))
    assert network.has_running_firewall() is False

    local.has('iptables', expect_args(['-S'], load_fixture('used_iptables')))
    assert network.has_running_firewall() is True

def test_is_domain_name_reachable(monkeypatch):
    local = LocalCommands()
    monkeypatch.setattr('mkcrowbar.network.local', local)

    local.has('ping', expect_args(['-c','1', 'fooo.net'], return_ok()))
    assert network.is_domain_name_reachable('fooo.net') is True

    local.has('ping', expect_args(['-c','1', 'fooooooo.net'], return_error()))
    assert network.is_domain_name_reachable('fooooooo.net') is False

