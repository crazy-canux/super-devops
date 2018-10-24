import unittest

from super_devops.ssh.paramiko_wrapper import BaseParamiko


class ParamikoTestCase(unittest.TestCase):
    @unittest.skip("ignore")
    def test_exec_command(self):
        with BaseParamiko('127.0.0.1', 'canux', 'canux') as ssh:
            output, error, rc = ssh.exec_command('ps -ef | grep -v grep | '
                                                 'grep sandbox | wc -l')
        print output, error, rc

    def test_start_service(self):
        with BaseParamiko('127.0.0.1', 'canux', 'canux') as ssh:
            output, error, rc = ssh.start_service('influxdb', 'influxd')
        print output, error, rc

    def test_stop_service(self):
        with BaseParamiko('127.0.0.1', 'canux', 'canux') as ssh:
            output, error, rc = ssh.stop_service('influxdb', 'inlfuxd')
        print output, error, rc


if __name__ == '__main__':
    unittest.main()
