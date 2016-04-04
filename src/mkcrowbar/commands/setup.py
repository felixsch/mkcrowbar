import subprocess
import os

from plumbum import cli
from mkcrowbar import MkCrowbar, paths
from mkcrowbar.pretty import fatal, step


@MkCrowbar.subcommand('setup')
class Setup(cli.Application):
    SUBCOMMAND_HELPMSG = False
    DESCRIPTION = 'Configure crowbar'

    def main(self, conf):
        self.interactive = self.parent.interactive

        if not os.path.exists(paths.crowbar_installer()):
            fatal('Could not find the installer', exit=False)
            fatal('Maybe you missed to prepare the environment before running setup')

        process = subprocess.Popen(paths.crowbar_installer() + " --verbose",
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   shell=True)
        with self.step('Running the installer') as s:
            for output in process.stdout:
                line = output.decode('utf-8').strip()

                if line.startswith('==='):
                    s.task(line[4:])
                if line.startswith('Error:'):
                    s.fail(line, exit=False)

                    # Show the complete error
                    for description in process.stdout:
                        desc = description.decode('utf-8').strip()
                        if desc.startswith('Crowbar installation terminated prematurely.'):
                            break
                        s.fail(desc, exit=False)
                    s.fail('Installation aborted.')

    def step(self, message):
        return step(message, interactive=self.interactive)

