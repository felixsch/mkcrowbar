from mkcrowbar import network, crowbar, base
from mkcrowbar.pretty import say


class Checks(base.App):
    DESCRIPTION = 'Check if everything is ready to bootstrap crowbar'

    def exec(self):
        iface = self.config.get('interface', 'eth0')

        say('Performing sanity checks')
        self.check_fqdn()
        self.check_ip_addrs(iface)

    def check_fqdn(self):
        with self.step('Check hostname and domain settings') as s:

            s.task('Check if hostname is fully qualified')
            hostname = network.hostname('-f')
            if not hostname:
                s.fail('The current hostname is not fully qualified. Check your network configuration')

            s.task('Check if domain name is set correctly')
            domain = network.hostname('-d')
            if not domain:
                s.fail('Unable to detect DNS domain name. Check your configuration')

            s.success("Your network setup seems valid.")

    def check_ip_addrs(self, iface):
        with self.step('Check ip addresses') as s:

            addr = network.iface_has_ipv4_addr(iface)

            s.task('Check resolved ip address')
            if not addr == self.config['network']['ipaddr']:
                s.fail('{} has wrong ip address associated. Check your network configuration'.format(iface))

            s.task('Check if ip address is no loopback address')
            if addr.split('.')[0] == '127':
                s.fail('Interface is bound to a loopback device. Check your network configuration'.format(iface))

            s.task('Validate crowbar network configuration')
            status = crowbar.network_config_valid(addr)
            if status is None:
                s.fail('Could not find network-json-validator. Maybe you missed to run mkcrowbar install <config>')
            if status[0] != 0:
                s.fail('Could not validate network crowbar network configuration', exit=False)
                s.fail(status[1])

            s.task('Check for running firewall.')
            if network.has_running_firewall():
                s.fail("A firewall is running, but crowbar is known to not work correctly with", exit=False)
                s.fail("with enabled SUSEFirewall. Disabling the firewall is recommend", exit=False)

            s.task('Validate that domain name is reachable')

            fqdn = network.hostname('-f')
            if not network.is_domain_name_reachable(fqdn):
                s.fail('Could not resolve the domainname. Check your network configuration')

            s.success('Ip address configuration seems valid.')
