import unittest

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from super_devops.wmi.wmi_wrapper import BaseWMI


class WMITest(unittest.TestCase):
    def test_run_cmd(self):
        with BaseWMI(
            host='127.0.0.1', domain='sv',
            username='Canux', password='******'
        ) as wmi:
            result = wmi.query("select * from meta_class where __class like '%win32%'")
        print result


if __name__ == '__main__':
    unittest.main()
