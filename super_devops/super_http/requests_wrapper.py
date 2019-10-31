import logging

from requests.sessions import Session
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3


logger = logging.getLogger(__name__)
logging.getLogger('requests').setLevel(logging.WARNING)


class BaseRequests(Session):

    """Customize requests for super-devops.

    with BaseRequests(username, password, domain) as req:
        res = req.get(url, **kwargs)
    res.status_code
    res.text
    """

    def __init__(self, username=None, password=None, domain=None):
        super(BaseRequests, self).__init__()

        self.auth = HTTPBasicAuth(username, password)
        # disable ssl verification
        self.verify = False

        self.domain = domain

        urllib3.disable_warnings()

    def get(self, url, **kwargs):
        kwargs.setdefault('timeout', 60)
        kwargs.setdefault('allow_redirects', True)
        return self.request('GET', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """POST method.

        :param data: post payload.
        :type data: dict.
        :param json: post payload json data.
        :type json: string.
        """
        kwargs.setdefault('timeout', 60)
        return self.request('POST', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        """PUT method.

        :param data: put payload.
        :type data: dict.
        """
        kwargs.setdefault('timeout', 60)
        return self.request('PUT', url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        """PATCH method.

        :param data: put payload.
        :type data: dict.
        """
        kwargs.setdefault('timeout', 60)
        return self.request('PATCH', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        kwargs.setdefault('timeout', 60)
        return self.request('DELETE', url, **kwargs)

    def options(self, url, **kwargs):
        kwargs.setdefault('timeout', 60)
        kwargs.setdefault('allow_redirects', True)
        return self.request('OPTIONS', url, **kwargs)

    def head(self, url, **kwargs):
        kwargs.setdefault('timeout', 60)
        kwargs.setdefault('allow_redirects', False)
        return self.request('HEAD', url, **kwargs)
