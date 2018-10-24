import urlparse
import logging

from super_devops.http.requests_wrapper import BaseRequests

logger = logging.getLogger(__name__)


class BaseKapacitor(object):
    def __init__(
            self, kapacitor_url="http://localhost:9091",
            username=None, password=None, domain=None
    ):
        self.kapacitor_url = kapacitor_url
        self.username = username
        self.password = password
        self.domain = domain

        self.base_url = urlparse.urljoin(
            self.kapacitor_url, "/kapacitor/v1/"
        )

    def config_influxdb(self, influxdb_url, influxdb_name="localhost"):
        try:
            url = urlparse.urljoin(
                self.base_url,
                "/config/influxdb/{}".format(influxdb_name)
            )
            payload = {
                "set": {
                    "urls": ["{}".format(influxdb_url)]
                }
            }
            with BaseRequests(
                    username=self.username, password=self.password,
                    domain=self.domain
            ) as req:
                res = req.post(url, data=payload)
                logger.debug(
                    "config influxdb for kapacitor: {}".format(res.content)
                )
            if res.status_code == 204:
                logger.info(
                    "Config influxdb {} for kapacitor succeed.".format(influxdb_name)
                )
                return True
            else:
                logger.error(
                    "Config influxdb {} for kapacitor failed.".format(influxdb_name)
                )
                return False
        except Exception:
            raise

    def config_smtp(
            self, enable=True, host="localhost", port=25,
            username="", password="",
            frm="mail.super-devops.com", to=["canuxcheng@gmail.com"]
    ):
        try:
            url = urlparse.urljoin(
                self.base_url, "/config/smtp/"
            )
            payload = {
                "set": {
                    "enabled": enable,
                    "host": host,
                    "port": int(port),
                    "username": username,
                    "password": password,
                    "from": "{}".format(frm),
                    "to": to
                }
            }
            with BaseRequests(
                    username=self.username, password=self.password,
                    domain=self.domain
            ) as req:
                res = req.post(url, data=payload)
                logger.debug(
                    "Config smtp for kapacitor: {}".format(res.content)
                )
            if res.status_code == 204:
                logger.info(
                    "Config smtp for kapacitor succeed."
                )
                return True
            else:
                logger.error(
                    "Config smtp for kapacitor failed."
                )
                return False
        except Exception:
            raise
