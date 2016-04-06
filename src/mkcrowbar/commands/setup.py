import subprocess
import os

from mkcrowbar import paths, base
from mkcrowbar.pretty import fatal, say


class Setup(base.App):
    DESCRIPTION = 'Configure crowbar'

    def exec(self):
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

                self.show(line)

                if line.startswith('==='):
                    s.task(line[4:])
                if line.startswith('Error:'):
                    s.fail(line, exit=False)
                    self.premature_error(s, process)
                if line.startswith('Crowbar installation terminated prematurely.'):
                    s.fail('Installer script failed unexpected. Try run mkcrowbar --verbose to see what happend')



    def premature_error(self, step, process):
        for description in process.stdout:
            desc = description.decode('utf-8').strip()
            if desc.startswith('Crowbar installation terminated prematurely.'):
                break
            step.fail(desc, exit=False)

        step.fail('Installation aborted.')

