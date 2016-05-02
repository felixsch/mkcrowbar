Vagrant.configure('2') do |config|
  config.vm.box = 'SLE-12'
  config.vm.provider :libvirt do |domain|
    domain.memory = 4096
    domain.cpus   = 2
  end
  config.vm.synced_folder '.', '/vagrant', disabled: true
  config.vm.synced_folder '.', '/mkcrowbar', type: 'nfs'
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network 'private_network', ip: '192.168.124.10'

  config.vm.provision :shell, inline: <<-SHELL
    echo "cd /mkcrowbar" >> /home/vagrant/.bashrc
    echo "sudo su"       >> /home/vagrant/.bashrc
  SHELL

end
