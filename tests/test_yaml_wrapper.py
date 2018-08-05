import unittest

from super_devops.yaml.yaml_wrapper import BaseYaml
import yaml


class BaseYamlTest(unittest.TestCase):
    @unittest.skip('ignore')
    def test_list(self):
        data = self.ctx.List["first"]
        print type(data)
        print data

    def test_dict(self):
        self.ctx = BaseYaml(r'C:\Users\wcheng\Desktop\Src\super-devops\etc\global.yaml')
        data = self.ctx.Dict["second"]
        print type(data)
        print data


if __name__ == '__main__':
    unittest.main()
