import unittest

from super_devops.grafana_stack.grafana_wrapper import BaseGrafana


class GrafanaTestCase(unittest.TestCase):
    @unittest.skip('ignore')
    def test_check_datasource_exist(self):
        grafana = BaseGrafana("http://127.0.0.1:3000", "admin",
                              "password")
        result = grafana.check_data_source_exist_by_name("devops")
        self.assertEqual(True, result, msg="check datasource exist failed.")

    def test_check_datasource_exist(self):
        grafana = BaseGrafana("http://127.0.0.1:3000",
                              'eyJrIjoiSU84dnphRGlOUTlaeGNCdTQ3clJlZjBxZG9IUFQ3cGoiLCJuIjoidGVzdCIsImlkIjoxfQ=='
                              )
        result = grafana.check_data_source_exist_by_name("devops")
        self.assertEqual(True, result, msg="check datasource exist failed.")



if __name__ == "__main__":
    unittest.main()
