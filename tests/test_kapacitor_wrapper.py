import unittest


import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from super_devops.tick_stack.kapacitor_wrapper import BaseKapacitor


class KapacitorTestCase(unittest.TestCase):
    def test_config_influxdb(self):
        pass

    def test_config_smtp(self):
        pass


if __name__ == "__main__":
    unittest.main()