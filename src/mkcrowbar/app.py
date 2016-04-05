import os
import sys

from plumbum import cli, colors
from mkcrowbar import commands, base


class MkCrowbar(base.App):

    def exec(self):
        self.check_privileges()
        self.register_commands()

        if not self.nested_command:
            return self.run_all()

    def check_privileges(self):
        user = os.getenv('SUDO_USER')
        root = os.getegid()

        if user is None and root != 0:
            print(colors.light_red | 'This programm requires root to run correctly')
            sys.exit(1)

    def register_commands(self):
        pass

    def run_all(self):
        schedule = [commands.Prepare, commands.Install, commands.Checks, commands.Setup]
        for command in schedule:
            (_, ret) = command.invoke(self.config_path, *self.flags())
            if ret:
                sys.exit(ret)


# Register all commands to mkcrowbar
MkCrowbar.subcommand('prepare', commands.Prepare)
MkCrowbar.subcommand('install', commands.Install)
MkCrowbar.subcommand('checks', commands.Checks)
MkCrowbar.subcommand('setup', commands.Setup)


def main():
    sys.exit(MkCrowbar.run())
