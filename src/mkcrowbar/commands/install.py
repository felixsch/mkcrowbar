from plumbum import cli
from mkcrowbar import zypper, MkCrowbar
from mkcrowbar.pretty import step, say, fatal


@MkCrowbar.subcommand('install')
class InstallCrowbar(cli.Application):
    SUBCOMMAND_HELPMSG = False
    DESCRIPTION        = 'Install crowbar on this maschine'

    def main(self, conf):
        self.config = self.parent.load_configuration(conf)
        self.interactive = self.parent.interactive

        say('Install basic requirements for running crowbar...')
        self.install_packages()

    def install_packages(self):
        with self.step('Install required packages') as s:
            s.task('refresh zypper database')
            status = zypper.refresh()

            if not status[0] == 0:
                s.fail('Could not refresh zypper database', 1)

            s.task('Installing basic crowbar packages')
            status = zypper.install(['crowbar', 'crowbar-core'])
            if not status[0] == 0:
                s.fail('Could not install required packages!', exit=False)
                warn(status[1])

            if status[0] == 4:
                fatal('Dependency problems occured. Check your media/sources..')
            if status[0] == 104:
                fatal('Could not find required packages. Check your your media/sources..')

            s.success('Installed packages successfully')

    def step(self, message):
        return step(message, interactive=self.interactive)
