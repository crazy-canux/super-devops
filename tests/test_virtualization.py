import unittest

from super_devops.virtualization.libvirt_wrapper import BaseLibvirt


default = """
<network>
  <name>default</name>
  <bridge name="virbr0"/>
  <forward/>
  <ip address="192.168.122.1" netmask="255.255.255.0">
    <dhcp>
      <range start="192.168.122.2" end="192.168.122.254"/>
    </dhcp>
  </ip>
</network>
"""

virbr1 = """
<network>
  <name>kvmnet1</name>
  <uuid>bb1fcb20-0d07-422c-b450-615b355c0e63</uuid>
  <bridge name='virbr1' stp='on' delay='0'/>
  <mac address='52:54:00:51:ab:64'/>
  <ip address='192.168.56.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.56.2' end='192.168.56.254'/>
    </dhcp>
  </ip>
</network>
"""


class VirtTestCase(unittest.TestCase):
    def test_init_libvirt(self):
        with BaseLibvirt(uri="qemu:///system") as vm:
            if vm.network_exist("default"):
                vm.destroy_network("default")
                vm.undefine_network("default")
            if vm.network_exist("kvmnet1"):
                vm.destroy_network("kvmnet1")
                vm.undefine_network("kvmnet1")
            if not vm.network_exist("default"):
                vm.define_network(default)
            if not vm.network_exist("kvmnet1"):
                vm.define_network(virbr1)


if __name__ == "__main__":
    unittest.main()