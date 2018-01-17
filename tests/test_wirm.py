import unittest

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from super_devops.winrm.pywinrm_wrapper import BaseWinRM


class WinRMTest(unittest.TestCase):
    def test_run_cmd(self):
        with BaseWinRM(
            host='10.103.16.75', domain='sv',
            username='WCheng', password='Wz1085694641', transport='ntlm'
        ) as winrm:
            # result = winrm.run_cmd("'ipconfig', ['/all']")
            result = winrm.run_cmd("dir")
        print result

    def test_run_ps(self):
        with BaseWinRM(
                host='10.103.16.75', domain='sv',
                username='WCheng', password='Wz1085694641', transport='ntlm'
        ) as winrm:
            result = winrm.run_ps("pwd")
        print result

if __name__ == '__main__':
    unittest.main()
