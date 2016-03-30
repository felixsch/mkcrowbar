import re
import os
import time

from plumbum          import local
from mkcrowbar.pretty import warn, fatal


def iface_has_ipv4_addr(iface):
    """
        Read the ipv4 address from the ip command
    """
    ip    = local['ip']['-f', 'inet', 'addr', 'show', iface]
    lines = ip().split('\n')
    if not len(lines) > 2:
        return None
    match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', lines[1])

    if not match:
        warn('Can not read ip address from `ip` command. This inidicates a bug!')
        fatal('Please open a issue at github')

    return match.group(1)


def iface_backup_configuration(iface):
    home = '/root/.mkcrowbar'
    path = '/etc/sysconfig/network/ifcfg-{}'.format(iface)

    if not os.path.exists(home):
        os.makedirs(home)

    if os.path.isfile(path):
        backup = '{}/ifcfg-{}.backup-{}'.format(home, iface, int(time.time()))
        os.rename(path, backup)


def iface_set_static_addr(iface, cfg):
    iface_backup_configuration(iface)

    with open('/etc/sysconfig/network/ifcfg-{}'.format(iface), 'w') as ifcfg:
        ifcfg.write('# Generated by mkcrowbar\n')
        ifcfg.write('# Backup files can be found in /root/.mkcrowbar\n')
        ifcfg.write('DEVICE={}\n'.format(iface))
        ifcfg.write("BOOTPROTO=static\n")

        for key, setting in cfg.items():
            ifcfg.write("{}={}\n".format(key.upper(), setting))

        ifcfg.write('ONBOOT=yes\n')


def iface_stop(iface):
    ifup = local['ifdown'][iface]
    status = ifup.run(retcode=None)
    if not status[0] == 0:
        return False
    return True


def iface_start(iface):
    ifup = local['ifup'][iface]
    status = ifup.run(retcode=None)
    if not status[0] == 0:
        return False
    return True


def iface_uses_dhcp(iface):
    """
        Checks if BOOTPROTO='dhcp' is set.
    """
    path = '/etc/sysconfig/network/ifcfg-{}'.format(iface)

    with open(path) as hdl:
        cfg   = hdl.read()
        match = re.search(r'BOOTPROTO=(\'|"|)(dhcp|static)(\'|"|)', cfg)

        if not match:
            warn('Could not check if network uses dhcp')
            return True

        if match.group(2) == 'dhcp':
            return True
    return False


def hostname(*args):
    """
        Get the current hostname
    """
    return local['hostname'][list(args)]().strip()


def set_hostname(new):
    """
        Set the hostname
    """
    hostname = local['hostname'][new]

    if hostname.run(retcode=None)[0] != 0:
        return False
    return True


def is_qualified_hostname(hostname):
    """
        Check if the hostname is fully qualified
    """
    is_domain = re.compile('^[a-zA-Z\d-]{,63}(\.([a-zA-Z\d-]{1,63}))+$')
    if not is_domain.match(hostname):
        return False
    return True


def add_to_hosts(ip, fqdn):
    """
        Add hostname to /etc/hosts if not already exists
    """
    with open('/etc/hosts', 'r+') as hdl:
        if fqdn in hdl.read():
            return -1
        hdl.write('{ip} {fqdn} {name}\n'.format(ip=ip, fqdn=fqdn, name=fqdn.split('.')[0]))
        return 0


def has_running_firewall():
    """
        Check if iptables shows other rules than -P <STREAM>
    """
    local.env['LANG'] = "C"
    iptables = local['iptables']['-S']
    output   = iptables().strip().split('\n')
    filtered = filter(lambda l: not l.startswith('-P'), output)
    lines    = list(filtered)

    if len(lines):
        return True
    return False


def is_domain_name_reachable(fqdn):
    """
        Sends one ICMP packages to fqdn to check if domain is reachable
    """
    ping   = local['ping']['-c', '1', fqdn]
    status = ping.run(retcode=None)

    if status[0] != 0:
        return False
    return True
