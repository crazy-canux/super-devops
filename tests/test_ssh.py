import unittest

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from super_devops.ssh.paramiko_wrapper import BaseParamiko


class ParamikoTest(unittest.TestCase):
    def test_exec_command(self):
        with BaseParamiko('127.0.0.1', 'canux', 'canux') as ssh:
            output, error, rc = ssh.exec_command('ps -ef | grep -v grep | '
                                                 'grep sandboxav | wc -l')
        print output, error, rc


if __name__ == '__main__':
    unittest.main()
