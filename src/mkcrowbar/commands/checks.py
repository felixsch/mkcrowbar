import sys

from plumbum          import cli, colors, local

from mkcrowbar        import pretty, network, MkCrowbar
from mkcrowbar.pretty import say, warn, info, fatal


@MkCrowbar.subcommand('check')
class PostInstallChecks(cli.Application):
   SUBCOMMAND_HELPMSG = False
   DESCRIPTION        = 'Check if everything is ready to bootstrap crowbar'

   def main(self, conf):
      self.config = self.parent.load_configuration(conf)

      iface = self.config.get('interface', 'eth0')

      say('Performing sanity checks')
      self.check_fqdn()
      self.check_ip_addrs(iface)
  

   def check_fqdn(self):
      with pretty.step('Check hostname and domain settings') as s:

         s.task('Check if hostname is fully qualified')
         hostname = network.hostname('-f')
         if not hostname:
            s.fail('The current hostname is not fully qualified. Check your network configuration')

         s.task('Check if domain name is set correctly')
         domain   = network.hostname('-d')
         if not domain:
            s.fail('Unable to detect DNS domain name. Check your configuration')

         s.success("Your network setup seems valid.")


   def check_ip_addrs(self, iface):
      with pretty.step('Check ip addresses') as s:

         s.task('Check resolved ip address')
         addr = network.iface_has_ipv4_addr(iface)
         if not addr == self.config['network']['ipaddr']:
            s.fail('{} has wrong ip address associated. Check your network configuration'.format(iface))
       
         s.task('Check if ip address is no loopback address')
         if addr.split('.')[0] == '127':
            s.fail('Interface is bound to a loopback device. Check your network configuration'.format(iface))

         s.task('Validate crowbar network configuration')
             
         s.task('Check for running firewall.')
         s.task('Validate that domain name is reachable')
         s.success('Ip address configuration seems valid.')


