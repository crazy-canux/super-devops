import unittest

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from super_devops.ssh.paramiko_wrapper import BaseParamiko


class ParamikoTest(unittest.TestCase):
    def test_exec_command(self):
        with BaseParamiko('127.0.0.1', 'canux', 'password') as ssh:
            output = ssh.exec_command('pwd')
        print output

    def test_exec_commands(self):
        with BaseParamiko('127.0.0.1', 'canux', 'password') as ssh:
            outputs = ssh.exec_commands(('pwd', 'ls'))
        for index, output in enumerate(outputs):
            print index, output

if __name__ == '__main__':
    unittest.main()
