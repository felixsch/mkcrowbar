from mkcrowbar import zypper, base
from mkcrowbar.pretty import say, fatal, warn


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

            packages = ['crowbar', 'crowbar-core', 'sqlite3']
            if len(self.config.get('crowbar-components', [])):
                packages += ["crowbar-" + comp for comp in self.config.get('crowbar-components')]

            status = zypper.install(packages)
            if not status[0] == 0:
                s.fail('Could not install required packages!', exit=False)
                warn(status[1])

            if status[0] == 4:
                fatal('Dependency problems occured. Check your media/sources..')
            if status[0] == 104:
                fatal('Could not find required packages. Check your your media/sources..')

            s.success('Installed packages successfully')


