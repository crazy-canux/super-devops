import unittest

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from super_devops.wmi.wmi_wrapper import BaseWMI
# wmic -U sv/WCheng%Wz1085694641 //192.168.1.4  "select * from Win32_ComputerSystem"


class WMITest(unittest.TestCase):
    def test_run_cmd(self):
        with BaseWMI(
            host='192.168.1.4', domain='sv',
            username='WCheng', password='Wz1085694641'
        ) as wmi:
            result = wmi.query("select * from Win32_ComputerSystem")
        print result


if __name__ == '__main__':
    unittest.main()
