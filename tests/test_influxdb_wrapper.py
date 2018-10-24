import unittest

from super_devops.tick_stack.influxdb_wrapper import BaseInfluxdb


class InfluxdbTestCase(unittest.TestCase):
    def test_check_database_exist(self):
        result = BaseInfluxdb().check_database_exist("sandboxav")
        self.assertEqual(True, result, msg="check database exist failed.")

    def test_create_database(self):
        result = BaseInfluxdb().create_database("sandboxav")
        self.assertEqual(True, result, msg="create database failed.")

    def test_create_rp(self):
        result = BaseInfluxdb().create_retention_policy(
            "sandboxav", "sandboxav", "30d", 2, True
        )
        self.assertEqual(True, result, msg="create rp failed.")


if __name__ == "__main__":
    unittest.main()
