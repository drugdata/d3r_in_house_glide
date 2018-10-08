# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  config.vm.box = "puppetlabs/centos-7.2-64-nocm"
  config.vm.provision :shell, path: "vagrantbootstrap.sh"
  config.ssh.forward_x11 = true
  config.disksize.size = '40GB'

  
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4092"
    vb.cpus = "2"
  end
end
