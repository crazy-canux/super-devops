import unittest

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from super_devops.ssh.paramiko_wrapper import BaseParamiko


class ParamikoTest(unittest.TestCase):
    def test_exec_command(self):
        with BaseParamiko('127.0.0.1', 'canux', 'password') as ssh:
            output, error, rc = ssh.exec_command('pwd')

    def test_exec_commands(self):
        with BaseParamiko('127.0.0.1', 'canux', 'password') as ssh:
            outputs, errors, rcs = ssh.exec_commands(('pwd', 'ls'))

if __name__ == '__main__':
    unittest.main()
