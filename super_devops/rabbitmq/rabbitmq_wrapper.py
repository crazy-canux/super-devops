import logging
import urllib.parse as urlparse

from super_devops.super_http.requests_wrapper import BaseRequests


logger = logging.getLogger(__name__)


class BaseRabbitmq(object):
    def __init__(
            self, url="http://localhost:15672/",
            username=None, password=None
    ):
        self.base_url = url
        self.username = username
        self.password = password

    def purge_queue(self, name, vhost="%2F"):
        try:
            url = urlparse.urljoin(
                self.base_url,
                "/api/queues/{}/{}/contents".format(vhost, name)
            )
            with BaseRequests(
                self.username, self.password
            ) as req:
                res = req.delete(url)
                logger.debug("purge queue res: {}".format(res.content))

            if res.status_code == 204:
                logger.debug("purge queue {} succeed.".format(name))
                return True
            else:
                logger.error("purge queue {} failed.".format(name))
                return False
        except Exception:
            raise


if __name__ == "__main__":
    rabbitmq = BaseRabbitmq(
        "http://localhost:15672", "sandbox", "password")
    rabbitmq.purge_queue(name="vmray_cloud")
