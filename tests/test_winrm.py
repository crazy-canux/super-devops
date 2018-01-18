import unittest

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from super_devops.winrm.pywinrm_wrapper import BaseWinRM


class WinRMTest(unittest.TestCase):
    def test_run_cmd(self):
        with BaseWinRM(
            host='192.168.1.4', domain='sv',
            #username='WCheng', password='password', transport='ntlm'
            username='WCheng', password='password'
        ) as winrm:
            result = winrm.run_cmd("ipconfig, /all")
        print result

    def test_run_ps(self):
        with BaseWinRM(
                host='127.0.0.1', domain='sv',
                username='Canux', password='******', transport='ntlm'
        ) as winrm:
            result = winrm.run_ps("ipconfig /all")
        print result

if __name__ == '__main__':
    unittest.main()
