from plumbum import cli
from mkcrowbar import config, pretty

class App(cli.Application):
    SUBCOMMAND_HELPMSG = False

    verbose = cli.Flag(['-v', '--verbose'], help='Show verbose output')
    interactive = cli.Flag(['--non-interactive'], help='Non interactive output')

    def main(self, conf):
        if conf:
            self.config = config.load(conf)
        self.config_path = conf

        if self.verbose:
            self.interative = False

        self.exec()

    def step(self, message):
        return pretty.step(message, interactive=self.interactive)

    def show(self, message):
        if self.verbose:
            print('> ' + message)

    def exec():
        pass
