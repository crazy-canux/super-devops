import unittest

from super_devops.yaml.yaml_wrapper import BaseYaml


class BaseYamlTest(unittest.TestCase):
    @unittest.skip('ignore')
    def test_list(self):
        data = self.ctx.List["first"]
        print type(data)
        print data

    @unittest.skip('ignore')
    def test_dict(self):
        self.ctx = BaseYaml(r'C:\Users\wcheng\Desktop\Src\super-devops\etc\global.yaml')
        data = self.ctx.Dict["second"]
        print type(data)
        print data

    @unittest.skip('ignore')
    def test_get_key(self):
        self.ctx = BaseYaml('/home/canux/Src/super-devops/etc/global.yaml')
        data = self.ctx.engine['threads'][0]
        print type(data)
        print data

    def test_shared(self):
        self.ctx = BaseYaml('/home/canux/Src/super-devops/etc/global.yaml')
        self.ctx.shared.test = "content"
        print self.ctx.shared["test"]


if __name__ == '__main__':
    unittest.main()
