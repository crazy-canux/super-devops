import unittest

from super_devops.winrm.pywinrm_wrapper import BaseWinRM


class WinRMTestCase(unittest.TestCase):
    def test_run_cmd(self):
        with BaseWinRM(
            host='127.0.0.1', domain='domain',
            username='username', password='password'
        ) as winrm:
            result = winrm.run_cmd("ipconfig, /all")
        self.assertIsNotNone(result, msg='run cmd failed')

    def test_run_ps(self):
        with BaseWinRM(
                host='127.0.0.1', domain='domain',
                username='username', password='password', transport='ntlm'
        ) as winrm:
            result = winrm.run_ps("ipconfig /all")
        self.assertIsNotNone(result, msg='run ps failed.')


if __name__ == '__main__':
    unittest.main()
