import yaml
import unittest


class YamlTestCase(unittest.TestCase):
    def test_load(self):
        data = yaml.load(open(r'C:\Users\wcheng\Desktop\Src\super-devops\etc\global.yaml', 'r'))
        print type(data)
        print data

    def test_safe_load(self):
        data = yaml.safe_load(open(r'C:\Users\wcheng\Desktop\Src\super-devops\etc\global.yaml', 'r'))
        print type(data)
        print data

    def test_load_all(self):
        data = yaml.load_all(open(r'C:\Users\wcheng\Desktop\Src\super-devops\etc\global.yaml', 'r'))
        print type(data)
        print data


if __name__ == '__main__':
    unittest.main()
