import unittest


from super_devops.tick_stack.kapacitor_wrapper import BaseKapacitor


class KapacitorTestCase(unittest.TestCase):
    def test_set_default_influxdb(self):
        pass

    def test_disable_smtp(self):
        kapacitor = BaseKapacitor(kapacitor_url="http://127.0.0.1:9092")
        result = kapacitor.disable_smtp()
        self.assertTrue(result, msg="disable failed")

    @unittest.skip("ignore")
    def test_enable_smtp(self):
        kapacitor = BaseKapacitor(kapacitor_url="http://127.0.0.1:9092")
        kapacitor.enable_smtp(frm="maf@company.com",
                              to=["cheng@canux.com"])


if __name__ == "__main__":
    unittest.main()
