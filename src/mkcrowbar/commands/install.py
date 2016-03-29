import sys

from plumbum          import cli, colors, local

from mkcrowbar        import pretty, zypper, MkCrowbar
from mkcrowbar.pretty import say, warn, info, fatal


@MkCrowbar.subcommand('install')
class InstallCrowbar(cli.Application):
   SUBCOMMAND_HELPMSG = False
   DESCRIPTION        = 'Install crowbar on this maschine'

   def main(self, conf):
      self.config = self.parent.load_configuration(conf)

      say('Install basic requirements for running crowbar...')
      self.install_packages()


   def install_packages(self):
     with pretty.step('Install required packages') as s:
        s.task('refresh zypper database')
        status = zypper.refresh()

        if not status[0] == 0:
           s.fail('Could not refresh zypper database', 1)
        
        s.task('Installing basic crowbar packages')
        status = zypper.install(['crowbar', 'crowbar-core'])
        if not status[0] == 0:
           s.fail('Could not install required packages!', exit=False)
           pretty.warn(status[1])

           if status[0] == 4:
              pretty.fatal('Dependency problems occured. Check your media/sources..')
           if status[0] == 104:
              pretty.fatal('Could not find required packages. Checkour your media/sources..')

        s.success('Installed packages successfully')
