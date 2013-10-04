# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.network :private_network, ip: "192.168.33.127"
  config.vm.synced_folder ".", "/vagrant", :nfs => true
  config.vm.provision :shell, :path => "scripts/bootstrap.sh"
  config.vm.network "forwarded_port", guest: 10002, host: 10002 
end
