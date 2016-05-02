import os

from mkcrowbar import paths
from plumbum.machines.local import local

def network_config_valid(ipv4):

    path = paths.crowbar_chef_templates('network')

    if os.path.exists(paths.crowbar_json('network')):
        path = paths.crowbar_json('network')

    validator = local['/opt/dell/bin/network-json-validator']

    try:
        return validator['--admin-ip', ipv4, path].run(retcode=None)

    except FileNotFoundError:
        return None
