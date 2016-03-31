from plumbum import cli

from mkcrowbar import network, crowbar, MkCrowbar
from mkcrowbar.pretty import say, step


@MkCrowbar.subcommand('configure')
class Configure(cli.Application):
    SUBCOMMAND_HELPMSG = False
    DESCRIPTION = 'Configure crowbar'

    def main(self, conf=None):
        if conf:
            ConfigureCrowbar.invoke(conf)
            ConfigureRepos.invoke(conf)

from mkcrowbar.commands.configure_crowbar import *
from mkcrowbar.commands.configure_repos import *
