from mkcrowbar import network, zypper, base
from mkcrowbar.pretty import say, info, fatal


class Prepare(base.App):
    DESCRIPTION        = 'Prepare host for crowbar installation'

    def exec(self):

        # hostname
        say('Configure hostname...')
        if not self.check_hostname() and self.config['hostname']:
            self.set_hostname()

        # ip
        say('Configure ip adress...')
        iface = self.config.get('interface', 'eth0')
        if not self.check_ip(iface) and self.config['network']:
            self.set_ip(iface)

        # use SUSEConnect or add repositories manually
        say('Enable sources for installation...')
        if self.config.get('use-connect', False):
            self.enable_products()
        else:
            self.enable_media()

        info('Your host is now prepared for crowbar.')
        info('You can now run mkcrowbar install <config>.')

    def check_ip(self, iface):
        addr  = network.iface_has_ipv4_addr(iface)

        if addr != self.config['network']['ipaddr']:
            info('Assigned ip address for {} does not match the configuration'.format(iface))
            info(' Current ip address is: {}'.format(addr))
            return False

        if network.iface_uses_dhcp(iface):
            info('Interface {} is configured to use dhcp. Need to switch to a static ip address'.format(iface))
            return False
        return True

    def check_hostname(self):
        hostname = network.hostname()

        if not network.is_qualified_hostname(self.config['hostname']):
            fatal('Invalid hostname in configuration found. Please specify a fully qualified hostname')

        if hostname != self.config['hostname']:
            info('Hostname does not match hostname specified in configuration.')
            return False

        return True

    def set_ip(self, iface):
        # reconfigure interface
        with self.step('Setting static ip address for interface {}'.format(iface)) as s:

            s.task('Reconfigure interface...')
            network.iface_set_static_addr(iface, self.config['network'])

            s.task('Stop interface...')
            if not network.iface_stop(iface):
                s.fail('Could not shutdown interface...')

            s.task('Start interface...')
            if not network.iface_start(iface):
                s.fail('Could not apply changes to interface {}'.format(iface))

            s.success('Successfully changed settings for {}'.format(iface))

    def set_hostname(self):
        with self.step('Setting hostname') as s:
            s.task("Setting hostname via hostname")
            if not network.set_hostname(self.config['hostname']):
                s.fail('Could not set hostname.')

            s.task('Adding ip to /etc/hosts')
            status = network.add_to_hosts(self.config['network']['ipaddr'], self.config['hostname'])
            if status == -1:
                s.done('Already exists')
            elif status == 0:
                s.done()
            else:
                s.fail('Could not add entry to /etc/hosts')
                s.success('Hostname successfully changed')

    def enable_media(self):
        with self.step('Enable media') as s:
            # Add sources
            for item in self.config.get('install-media', []):

                # extended source definition
                if isinstance(item, dict):
                    if len(item) > 1:
                        s.fail('Invalid syntax in configuration file. One settings definition per source')
                    for alias, settings in item.items():
                        if 'repo' not in settings:
                            s.fail('{} has no repo set. Please update your configuration'.format(alias))

                        repo = settings.pop('repo', None)
                        settings = settings

                        s.task('Enable {}...'.format(alias))

                        status = zypper.repo_enable(repo, alias, settings)
                else:
                    status = zypper.repo_enable(item)

                if status[0] == 0:
                    s.done('done')
                elif status[0] == 4:
                    s.done('already exists')
                else:
                    s.fail('Adding repository failed', exit=False)
                    fatal(status[2])

            s.task('Refresh zypper database')
            status = zypper.refresh()

            if not status[0] == 0:
                s.fail('Could not refresh database... ({})'.format(status[2]))

            s.success('Media/Repositories successfully enabled')

    def enable_products(self):
        pass
