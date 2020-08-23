import logging
import hashlib

from tqdm import tqdm
from requests.sessions import Session
from requests.packages import urllib3
from requests.auth import AuthBase, HTTPBasicAuth


logger = logging.getLogger(__name__)
logging.getLogger('requests').setLevel(logging.WARNING)


class SessionAuth(AuthBase):
    def __init__(self, session_id):
        if not session_id:
            session_id = ''
        self.session_id = session_id

    def __call__(self, r):
        r.headers['Authorization'] = self.session_id
        return r


class BaseRequests(Session):

    """Customize requests for super-devops.

    with BaseRequests(username, password, domain) as req:
        res = req.get(url, **kwargs)
    res.status_code
    res.text
    """

    def __init__(self, username=None, password=None,
                 domain=None, session_id=None):
        super(BaseRequests, self).__init__()

        if session_id:
            self.auth = SessionAuth(session_id)
        elif username and password:
            self.auth = HTTPBasicAuth(username, password)

        self.domain = domain

        urllib3.disable_warnings()

    def get(self, url, params=None, **kwargs):
        kwargs.setdefault('timeout', 60)
        kwargs.setdefault('allow_redirects', True)
        return self.request('GET', url, params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """POST method.

        :param data: post payload.
        :type data: dict.
        :param json: post payload json data.
        :type json: string.
        """
        kwargs.setdefault('timeout', 60)
        kwargs.setdefault('allow_redirects', True)
        return self.request('POST', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        """PUT method.

        :param data: put payload.
        :type data: dict.
        """
        kwargs.setdefault('timeout', 60)
        kwargs.setdefault('allow_redirects', True)
        return self.request('PUT', url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        """PATCH method.

        :param data: put payload.
        :type data: dict.
        """
        kwargs.setdefault('timeout', 60)
        kwargs.setdefault('allow_redirects', True)
        return self.request('PATCH', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        kwargs.setdefault('timeout', 60)
        kwargs.setdefault('allow_redirects', True)
        return self.request('DELETE', url, **kwargs)

    def options(self, url, **kwargs):
        kwargs.setdefault('timeout', 60)
        kwargs.setdefault('allow_redirects', True)
        return self.request('OPTIONS', url, **kwargs)

    def head(self, url, **kwargs):
        kwargs.setdefault('timeout', 60)
        kwargs.setdefault('allow_redirects', False)
        return self.request('HEAD', url, **kwargs)

    def download(self, url, filename, chunk_size=4096, params=None, **kwargs):
        try:
            proxies = {
                'http': None,
                'https': None
            }
            kwargs.setdefault('timeout', None)
            kwargs.setdefault('allow_redirects', True)
            kwargs.setdefault('verify', False)
            kwargs.setdefault('stream', True)
            kwargs.setdefault('proxies', proxies)
            md5_obj = hashlib.md5()
            with open(filename, 'wb') as f:
                for block in self.request('GET', url, params, **kwargs).iter_content(chunk_size):
                    f.write(block)
                    md5_obj.update(block)
            return md5_obj.hexdigest()
        except Exception:
            raise

