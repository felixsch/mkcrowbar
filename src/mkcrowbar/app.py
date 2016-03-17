from plumbum           import cli, colors
from mkcrowbar.pretty  import fatal

import os
import sys
import yaml


class MkCrowbar(cli.Application):
   verbose      = cli.Flag(['-v', '--verbose'], help = 'Show verbose output')

   def main(self, *args):
      if args or not self.nested_command:
         fatal('Unknown or no command given', exit=False)
         self.help()
         return 1 

      self.check_privileges()

   def check_privileges(self):
      user = os.getenv('SUDO_USER')
      root = os.getegid()

      if user is None and root != 0:
         print(colors.light_red | 'This programm requires root to run correctly')
         sys.exit(1)

   def load_configuration(self, path=None):
      if not path:
         path = os.environ.get('MKCROWBAR_CONFIG')

      if not path:
         fatal('You need to specify a configuration file')

      if not os.path.isfile(path):
         fatal('Could not open configuration file (No such file)')

      try:
         self.config = yaml.safe_load(open(path))

         self.validate_configuration()
      except yaml.scanner.ScannerError as e:
         fatal('Parsing configuration file failed: {}'.format(e))

      return self.config

   def validate_configuration(self):
      required = ['hostname', 'interface', 'network']

      for key in required:
         if not key in self.config:
            fatal("Configuration option '{}' is mandatory. Please update your configuration".format(key))

         
      




def main():
   sys.exit(MkCrowbar.run())
