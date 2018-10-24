import unittest

from super_devops.wmi.wmi_wrapper import BaseWMI
# wmic -U domain/username%password //127.0.0.1  "select * from Win32_ComputerSystem"


class WMITestCase(unittest.TestCase):
    def test_run_cmd(self):
        with BaseWMI(
            host='127.0.0.1', domain='domain',
            username='username', password='password'
        ) as wmi:
            result = wmi.query("select * from Win32_ComputerSystem")
        print result


if __name__ == '__main__':
    unittest.main()
