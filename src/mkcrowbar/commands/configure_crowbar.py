from plumbum import cli

from mkcrowbar import network, crowbar, MkCrowbar
from mkcrowbar.pretty import say, step
from mkcrowbar.commands.configure import Configure


@Configure.subcommand('crowbar')
class ConfigureCrowbar(cli.Application):
    SUBCOMMAND_HELPMSG = False
    DESCRIPTION = 'Configure crowbar'

    def main(self, conf):
        print("configure crowbar")
