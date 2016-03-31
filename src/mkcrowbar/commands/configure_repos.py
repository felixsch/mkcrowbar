
from plumbum import cli

from mkcrowbar import network, crowbar, MkCrowbar
from mkcrowbar.pretty import say, step
from mkcrowbar.commands.configure import Configure


@Configure.subcommand('repos')
class ConfigureRepos(cli.Application):
    SUBCOMMAND_HELPMSG = False
    DESCRIPTION = 'Configure repositories'

    def main(self, conf):
        print("configure repo")
