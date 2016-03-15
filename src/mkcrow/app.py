from plumbum import cli, colors

import os
import sys

class MkCrow(cli.Application):
   verbose = cli.Flag(['-v', '--verbose'], help = 'Show verbose output')

   def main(self):
      self.check_privileges()

   def check_privileges(self):
      user = os.getenv('SUDO_USER')
      root = os.getegid()

      if user is None and root != 0:
         print(colors.light_red | 'This programm requires root to run correctly')
         sys.exit(1)


def main():
   sys.exit(MkCrow.run())
