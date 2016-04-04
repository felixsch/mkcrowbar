

def barclamps(git_install=False):
    if git_install:
        return '/root/crowbar/barclamps'
    return '/opt/dell/barclamps'


def crowbar_json(name, git_install=False):
    path = '/etc/crowbar/'
    if git_install:
        path = '/root/crowbar/'
    return path + name + '.json'


def crowbar_chef_templates(name):
    path = '/opt/dell/chef/data_bags/crowbar/bc-template-'
    return path + name + '.json'


def crowbar_installer():
    return '/opt/dell/bin/install-chef-suse.sh'


def repository_path(version, repository):
    base = '/srv/tftpboot/' + version + '/'
    if repository == 'install':
        return base + 'install'
    return base + 'repos/' + repository
