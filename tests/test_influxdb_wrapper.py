import unittest

from super_devops.tick_stack.influxdb_wrapper import BaseInfluxdb


class InfluxdbTestCase(unittest.TestCase):
    @unittest.skip('ignore')
    def test_check_database_exist(self):
        result = BaseInfluxdb().check_database_exist("devops")
        self.assertEqual(True, result, msg="check database exist failed.")

    @unittest.skip('ignore')
    def test_create_database(self):
        result = BaseInfluxdb().create_database("sandboxav")
        self.assertEqual(True, result, msg="create database failed.")

    @unittest.skip('ignore')
    def test_create_rp(self):
        result = BaseInfluxdb().create_retention_policy(
            "sandboxav", "sandboxav", "30d", 2, True
        )
        self.assertEqual(True, result, msg="create rp failed.")

    def test_query(self):
        ifql = """
        SELECT 100 - mean("usage_idle") AS "idle" 
        FROM "cpu" 
        WHERE "cpu" = 'cpu-total' AND  time > now() - 5m
        GROUP BY time(1m), "host" fill(none)
        """
        result = BaseInfluxdb().query("devops", ifql)
        self.assertIsNotNone(result, 'select failed.')


if __name__ == "__main__":
    unittest.main()
