from plumbum import cli
from mkcrowbar import config, pretty

class App(cli.Application):
    SUBCOMMAND_HELPMSG = False

    verbose = cli.Flag(['-v', '--verbose'], help='Show verbose output')
    interactive = cli.Flag(['--non-interactive'], help='Non interactive output', default=True)

    def main(self, conf):
        if conf:
            self.config = config.load(conf)
        self.config_path = conf

        self.exec()

    def step(self, message):
        return pretty.step(message, interactive=self.interactive)

    def exec():
        pass
