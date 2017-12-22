import yaml
import unittest


class YamlTest(unittest.TestCase):
    def test_load(self):
        data = yaml.load(open('/home/canux/Src/taf/etc/global.yaml', 'r'))
        print type(data)
        print data


if __name__ == '__main__':
    unittest.main()