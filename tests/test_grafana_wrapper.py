import unittest

from super_devops.grafana.grafana_wrapper import BaseGrafana


class GrafanaTestCase(unittest.TestCase):
    @unittest.skip('ignore')
    def test_check_datasource_exist(self):
        grafana = BaseGrafana("http://10.103.64.207:3000", "sandbox",
                              "password")
        result = grafana.check_data_source_exist_by_name("MAF")
        self.assertEqual(True, result, msg="check datasource exist failed.")

    def test_check_datasource_exist(self):
        grafana = BaseGrafana("http://10.103.64.207:3000",
                              'eyJrIjoiSU84dnphRGlOUTlaeGNCdTQ3clJlZjBxZG9IUFQ3cGoiLCJuIjoidGVzdCIsImlkIjoxfQ=='
                              )
        result = grafana.check_data_source_exist_by_name("MAF")
        self.assertEqual(True, result, msg="check datasource exist failed.")



if __name__ == "__main__":
    unittest.main()
