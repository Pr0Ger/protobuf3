VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty32"

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "init_test_vm.yml"
    ansible.sudo = true
  end
end
