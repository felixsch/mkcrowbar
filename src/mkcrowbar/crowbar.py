import os

from plumbum   import local
from mkcrowbar import paths

def network_config_valid(ipv4):
   
   path = paths.crowbar_chef_templates('network')
   
   if os.path.exists(paths.crowbar_json('network')):
      path = paths.crowbar_json('network')

   validator = local['/opt/dell/bin/network-json-validator']

   return validator['--admin-ip', ipv4, path].run(retcode=None)
