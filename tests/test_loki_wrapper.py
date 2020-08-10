import unittest

from super_devops.grafana_stack.loki_wrapper import BaseLoki


class LokiTestCase(unittest.TestCase):
    def test_query(self):
        loki = BaseLoki("http://127.0.0.1:3000")
        loki.query(query="{app='CSa'}")

    def test_push(self):
        streams = {
            "streams": [
                {
                    "stream": {
                        "app": "CSa"
                    },
                    "values": [
                        ["1570818238000000000", "fizzbuzz"]
                    ]
                }
            ]
        }
        loki = BaseLoki("http://127.0.0.1:3000")
        loki.push(streams)


if __name__ == "__main__":
    unittest.main()
