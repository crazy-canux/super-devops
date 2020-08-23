import logging
import urllib.parse as urlparse

from base.requests_wrapper import BaseRequests

logger = logging.getLogger(__name__)


class BaseRegistry(object):
    def __init__(self, url, username=None, password=None, domain=None, version="v2"):
        self.url = urlparse.urljoin(url, version+"/")
        self.username = username
        self.password = password
        self.domain = domain
        self.headers = {}
        # "Content-Type": "application/json"

    def ping(self):
        try:
            with BaseRequests(self.username, self.password, self.domain) as req:
                resp = req.get(self.url, **{"headers": self.headers, 'verify': False})
            if resp.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            logger.error("check endpoint implements docker registry api failed: {}".format(e.args))

    def list_repo(self):
        try:
            url = urlparse.urljoin(self.url, "_catalog")
            with BaseRequests(self.username, self.password, self.domain) as req:
                resp = req.get(url, **{"headers": self.headers, 'verify': False})
            if resp.status_code == 200:
                return resp.json()
            else:
                logger.error("list repository failed: {}".format(resp.reason))
        except Exception as e:
            logger.error("list repositories failed: {}".format(e.args))

    def list_tags(self, name):
        try:
            url = urlparse.urljoin(self.url, "{}/tags/list".format(name))
            with BaseRequests(self.username, self.password, self.domain) as req:
                resp = req.get(url, **{"headers": self.headers, 'verify': False})
            if resp.status_code == 200:
                return resp.json()
            else:
                logger.error("list tags failed: {}".format(resp.reason))
        except Exception as e:
            logger.error("list tags for {} failed: {}".format(name, e.args))

    def get_manifests(self, name, reference):
        try:
            url = urlparse.urljoin(self.url, "{}/manifests/{}".format(name, reference))
            with BaseRequests(self.username, self.password, self.domain) as req:
                resp = req.get(url, **{"headers": self.headers, 'verify': False, 'stream': True})
            if resp.status_code == 200:
                return resp
            else:
                logger.error("get manifests failed: {}".format(resp.reason))
        except Exception as e:
            logger.error("get manifests for {}/{} failed: {}".format(name, reference, e.args))

    def put_manifests(self, name, reference):
        try:
            url = urlparse.urljoin(self.url, "{}/manifests/{}".format(name, reference))
            with BaseRequests(self.username, self.password, self.domain) as req:
                resp = req.put(url)
        except Exception as e:
            logger.error("put manifests for {}/{} failed: {}".format(name, reference, e.args))

    def delete_manifests(self, name, reference):
        try:
            url = urlparse.urljoin(self.url, "{}/manifests/{}".format(name, reference))
            with BaseRequests(self.username, self.password, self.domain) as req:
                resp = req.delete(url)
        except Exception as e:
            logger.error("delete manifests for {}/{} failed: {}".format(name, reference, e.args))

    def get_blobs(self, name, digest):
        try:
            url = urlparse.urljoin(self.url, "{}/blobs/{}".format(name, digest))
            with BaseRequests(self.username, self.password, self.domain) as req:
                resp = req.get(url, **{"headers": self.headers, 'verify': False, 'stream': True})
            if resp.status_code == 200:
                return resp
            else:
                logger.error("get blobs failed: {}".format(resp.reason))
        except Exception as e:
            logger.error("get blobs for {}/{} failed: {}".format(name, digest, e.args))

    def post_blobs(self, name, digest):
        try:
            url = urlparse.urljoin(self.url, "{}/blobs/{}".format(name, digest))
            with BaseRequests(self.username, self.password, self.domain) as req:
                resp = req.post(url)
        except Exception as e:
            logger.error("post blobs for {}/{} failed: {}".format(name, digest, e.args))

    def delete_blobs(self, name, digest):
        try:
            url = urlparse.urljoin(self.url, "{}/blobs/{}".format(name, digest))
            with BaseRequests(self.username, self.password, self.domain) as req:
                resp = req.delete(url)
        except Exception as e:
            logger.error("delete blobs for {}/{} failed: {}".format(name, digest, e.args))

