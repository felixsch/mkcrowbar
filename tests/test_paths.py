from mkcrowbar import paths


def test_crowbar_json():
    assert paths.crowbar_json('somejson') == '/etc/crowbar/somejson.json'


def test_crowbar_chef_template():
    file_path = '/opt/dell/chef/data_bags/crowbar/bc-template-template.json'
    assert paths.crowbar_chef_templates('template') == file_path


def test_crowbar_installer():
    installer_path = '/opt/dell/bin/install-chef-suse.sh'
    assert paths.crowbar_installer() == installer_path


def test_crowbar_installer_state():
    state_file = '/var/lib/crowbar/install/crowbar-install-failed'
    assert paths.crowbar_installer_state('failed') == state_file


def test_repository_path():
    install_repo = '/srv/tftpboot/suse-12.1/x86_64/install'
    test_repo = '/srv/tftpboot/suse-12.0/s390x/repos/test'

    assert paths.repository_path('suse-12.1', 'install') == install_repo
    assert paths.repository_path('suse-12.0', 'test', 's390x') == test_repo
