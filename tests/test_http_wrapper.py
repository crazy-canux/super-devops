import unittest
import json

from super_devops.http.requests_wrapper import BaseRequests


class RequestsTestCase(unittest.TestCase):
    @unittest.skip('passed')
    def test_get(self):
        url = 'http://127.0.0.1:8888/files'
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
        url = 'http://127.0.0.1:8888/files'
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
        url = 'http://127.0.0.1:8080/api/verify'
        with BaseRequests() as req:
            res = req.post(
                url,
                **{
                    'files': {
                        'file': open('/etc/test/config.ini', 'rb'),
                    }
                }
            )
        print res.status_code
        print res.text
        print res.headers

    @unittest.skip('passed')
    def test_post_files(self):
        url = "http://127.0.0.1/api?sn=123456789ABC&key" \
              "=2813babc6ed843c1a496349f2a53d8db"
        with BaseRequests() as req:
            res = req.post(
                url,
                data={
                    "MethodInput": json.dumps({"sessiontype": "webui"}),
                    "MethodName": "SubmitTask"
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
        url = "http://127.0.0.1/JsonData.aspx"
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

