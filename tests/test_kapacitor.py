import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(".."))
from super_devops.http.requests_wrapper import BaseRequests


class KapacitorTestCase(unittest.TestCase):
    def test_get_smtp(self):
        with BaseRequests() as req:
            res = req.get("http://10.103.239.60:9092/kapacitor/v1/config"
                          "/smtp/")
        print res.status_code
        print res.content


if __name__ == "__main__":
    unittest.main()
