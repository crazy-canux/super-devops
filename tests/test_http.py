import unittest
import json

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from super_devops.http.requests_wrapper import BaseRequests


class RequestsTest(unittest.TestCase):
    @unittest.skip('passed')
    def test_get(self):
        """Test reversinglabs server."""
        url = 'http://10.103.239.43:8888/files'
        with BaseRequests() as req:
            res = req.get(
                url,
                **{
                    'cookies': {
                        'authCode': 'a3e67c051cb499e83e96a7c6ddf301e9',
                    },
                }
            )
        print res.status_code
        print res.text
        print res.headers

    @unittest.skip('passed')
    def test_post(self):
        """Test reversinglabs server."""
        url = 'http://10.103.239.46:8888/files'
        with BaseRequests() as req:
            res = req.post(
                url,
                data={
                    "pagesize": "30",
                    "pageindex": "0",
                    "sortkey": "updatetime"
                },
                **{
                    'cookies': {
                        'authCode': 'a3e67c051cb499e83e96a7c6ddf301e9',
                    },
                }
            )
        print res.status_code
        print res.text
        print res.headers

    @unittest.skip("passed")
    def test_post_file(self):
        """Test PE verify server."""
        url = 'http://10.103.239.70:8080/api/verify'
        with BaseRequests() as req:
            res = req.post(
                url,
                **{
                    'files': {
                        'file': open('/opt/sandboxav/etc/sboxconfig.ini','rb'),
                    }
                }
            )
        print res.status_code
        print res.text
        print res.headers

    @unittest.skip('passed')
    def test_post_files(self):
        """Test capture dashboard api."""
        url = "http://10.103.239.46/api?sn=123456789ABC&key" \
              "=2813babc6ed843c1a496349f2a53d8db"
        with BaseRequests() as req:
            res = req.post(
                url,
                data={
                    "MethodInput": json.dumps({"sessiontype": "webui"}),
                    "MethodName": "SubmitTask2"
                },
                **{
                    'files': {
                        'FileStream': open(
                            '/home/canux/Src/super-devops/tools/geckodriver-v0.19.0-linux64.tar.gz', 'rb'
                        ),
                    }
                }
            )
        print res.status_code
        print res.text
        print res.headers

    def test_updatethreadconfig(self):
        url = "http://10.103.239.62/JsonData.aspx"
        with BaseRequests() as req:
            res = req.post(
                url,
                data=json.dumps({
                    "MethodInput": {},
                    "MethodName": "GetThreadConfig"
                }),
                **{
                    'headers': {'content-type': 'application/json'},
                }
            )
        print res.status_code
        print res.text
        print res.headers


if __name__ == "__main__":
    unittest.main()

