from mkcrowbar import zypper, base
from mkcrowbar.pretty import say, fatal


class Install(base.App):
    DESCRIPTION = 'Install crowbar on this maschine'

    def exec(self):
        say('Install basic requirements for running crowbar...')
        self.install_packages()

    def install_packages(self):
        with self.step('Install required packages') as s:
            s.task('refresh zypper database')
            status = zypper.refresh()

            if not status[0] == 0:
                s.fail('Could not refresh zypper database', 1)

            s.task('Installing basic crowbar packages')
            s.note('This takes a while')

            (install, remove) = self.select_packages()

            self.show('installing packages = {}'.format(install))

            status = zypper.install(install)
            if not status[0] == 0:
                s.fail('Could not install required packages!', exit=False)
                s.fail(status[1])

            if status[0] == 4:
                fatal('Dependency problems occured. Check your media/sources..')
            if status[0] == 104:
                fatal('Could not find required packages. Check your your media/sources..')

            s.done('Installed packages successfully')

            s.task('Removing conflicting packages')
            self.show("Removing packages = {}".format(remove))
            status = zypper.remove(remove)

            if status[0] != 0 and status[0] != 104:
                s.fail('Could not remove conflicting packages', exit=False)
                s.fail(status[1])
            s.done('Conflicting packages removed')

    def select_packages(self):
        install = ['crowbar', 'sqlite3', 'crowbar-core', 'ntp']
        remove = []

        if self.config['installation'] == 'storage':
            install += ['crowbar-ses', 'patterns-ses-admin']
            remove += ['syslog-ng']

        if self.config['installation'] == 'cloud':
            install += ['patterns-cloud-admin']

        if len(self.config.get('crowbar-components', [])):
            install += ["crowbar-" + comp for comp in self.config.get('crowbar-components')]

        return (install, remove)
