import os

from plumbum import cli, local
from mkcrowbar import MkCrowbar, zypper, paths
from mkcrowbar.pretty import step


@MkCrowbar.subcommand('repos')
class SetupRepositories(cli.Application):
    SUBCOMMAND_HELPMSG = False
    DESCRIPTION = 'Initialize crowbar repositories'

    def main(self, conf):
        self.interactive = self.parent.interactive
        self.config = self.parent.load_configuration(conf)

        with self.step('Enable crowbar repositories') as s:
            repos = self.config.get('repositories', {})

            if not self.has_repo_name('install'):
                s.fail('You need to specify at least the installation repository')

            if self.has_repo_type('createrepo'):
                s.task('Installing createrepo')
                if not self.install_createrepo():
                    s.fail('Could not install create repo. Check your system status')

            for repo in repos:
                if 'version' not in repo:
                    s.fail('Missing version specification. Your need to add a version for {}'.format(repo['name']))

                s.task('Prepairing {repo} ({version})...'.format(repo=repo['name'], version=repo['version']))
                if repo['type'] == 'nfs':
                    self.mount_nfs(s, repo)
                elif repo['type'] == 'rsync':
                    self.rsync_repo(s, repo)
                elif repo['type'] == 'createrepo':
                    self.create_repo(s, repo)
                else:
                    s.fail('Unknown repository type. Check your configuration')

    def step(self, message):
        return step(message, interactive=self.interactive)

    def mount_nfs(self, step, repo):
        name = repo['name']
        version = repo['version']
        mount = local['mount']

        if not os.path.exists(paths.repository_path(version, name)):
            step.note('Creating directory')
            os.makedirs(paths.repository_path(version, name))

        step.note('Mounting the repository')

        mount_nfs = mount['-t', 'nfs', repo['source'], paths.repository_path(version, name)]
        status = mount_nfs.run(retcode=None)

        if status[0] == 32:
            step.done('Already mounted or busy')
        elif status[0] != 0:
            step.fail(status[2].strip(), exit=False)
            step.fail('Could not mount nfs share')

    def rsync_repo(self, step, repo):
        pass

    def create_repo(self, step, repo):
        pass

    def has_repo_name(self, repo_name):
        repo_names = [repo['name'] for repo in self.config.get('repositories')]
        if repo_name not in repo_names:
            return False
        return True

    def has_repo_type(self, repo_type):
        repo_types = [repo['type'] for repo in self.config.get('repositories')]
        if repo_type not in repo_types:
            return False
        return True

    def install_createrepo(self):
        status = zypper.install(['createrepo'])
        if not status[0] == 0:
            return False
        return True
