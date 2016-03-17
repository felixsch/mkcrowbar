
Vagrant.configure('2') do |config|
  config.vm.box = 'SLE-12'
  config.vm.provider :libvirt
  config.vm.synced_folder ".", "/mkcrow", type: "nfs"
  config.vm.network "private_network", ip: "192.168.124.10"
end
