import os
import sys

from plumbum import cli, colors
from mkcrowbar import commands, config


class MkCrowbar(cli.Application):

    verbose = cli.Flag(['-v', '--verbose'], help='Show verbose output')
    interactive = cli.Flag(['--non-interactive'], help='Non interactive output', default=True)

    def main(self, conf=None):

        if self.verbose:
            self.interactive = False

        self.check_privileges()

        # run all steps
        if conf and not self.nested_command:
            self.config = config.load(conf)
            self.config_path = conf
            return self.run_all()

        if not self.nested_command:
            return self.help()

    def check_privileges(self):
        user = os.getenv('SUDO_USER')
        root = os.getegid()

        if user is None and root != 0:
            print(colors.light_red | 'This programm requires root to run correctly')
            sys.exit(1)


    # This makes definitly no sense but plumbum inverses the default value
    # wenn a flag value is set. So we only need to set the key if we want to
    # trigger the flag.
    def flags(self):
        f = {}
        if self.verbose:
            f['verbose'] = True
        if self.interactive:
            f['interactive'] = True
        return f



    def run_all(self):
        schedule = [commands.Prepare, commands.Install, commands.Checks, commands.Repos, commands.Setup]
        for command in schedule:
            (_, ret) = command.invoke(self.config_path, **self.flags())
            if ret:
                sys.exit(ret)


# Register all commands to mkcrowbar
MkCrowbar.subcommand('prepare', commands.Prepare)
MkCrowbar.subcommand('install', commands.Install)
MkCrowbar.subcommand('checks', commands.Checks)
MkCrowbar.subcommand('repos', commands.Repos)
MkCrowbar.subcommand('setup', commands.Setup)


def main():
    sys.exit(MkCrowbar.run())
