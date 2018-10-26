import urlparse
import logging
import json

from super_devops.http.requests_wrapper import BaseRequests

logger = logging.getLogger(__name__)


class BaseKapacitor(object):
    def __init__(
            self, kapacitor_url="http://localhost:9092",
            username=None, password=None, domain=None
    ):
        self.kapacitor_url = kapacitor_url
        self.username = username
        self.password = password
        self.domain = domain

        self.base_url = urlparse.urljoin(
            self.kapacitor_url, "/kapacitor/v1"
        )

    def set_influxdb(
            self, influxdb_url="http://localhost:8086",
            name="localhost", default=True, enabled=True,
            username="", password="", timeout=0
    ):
        try:
            url = self.base_url + "/config/influxdb/{}".format(name)
            logger.debug("url: {}".format(url))
            payload = json.dumps({
                "set": {
                    "default": default,
                    "enabled": enabled,
                    "name": name,
                    "username": username,
                    "password": password,
                    "timeout": timeout,
                    "urls": ["{}".format(influxdb_url)]
                }
            })
            logger.debug("payload: {}".format(payload))
            with BaseRequests(
                    username=self.username, password=self.password,
                    domain=self.domain
            ) as req:
                res = req.post(url, data=payload)
                logger.debug(
                    "config influxdb for kapacitor res: {}".format(res.content)
                )
                logger.debug(
                    "Config influxdb for kapacitor status_code: {}".format(res.status_code)
                )
            if res.status_code == 204:
                logger.info(
                    "Config influxdb {} for kapacitor succeed.".format(name)
                )
                return True
            else:
                logger.error(
                    "Config influxdb {} for kapacitor failed.".format(name)
                )
                return False
        except Exception:
            raise

    def set_smtp(
            self, enable=True, host="localhost", port=25,
            frm="mail.super-devops.com", to=["canuxcheng@gmail.com"],
            username="", password="", no_verify=True, idle_timeout="30s",
            global_enable=True, state_changes_only=True
    ):
        try:
            url = self.base_url + "/config/smtp/"
            logger.debug("url: {}".format(url))
            payload = json.dumps({
                "set": {
                    "enabled": enable,
                    "host": host,
                    "port": int(port),
                    "username": username,
                    "password": password,
                    "to": to,
                    "from": frm,
                    "no-verify": no_verify,
                    "global": global_enable,
                    "idle-timeout": idle_timeout,
                    "state-changes-only": state_changes_only
                }
            })
            with BaseRequests(
                    username=self.username, password=self.password,
                    domain=self.domain
            ) as req:
                res = req.post(url, data=payload)
                logger.debug(
                    "Config smtp for kapacitor res: {}".format(res.content)
                )
                logger.debug(
                    "Config smtp for kapacitor status_code: {}".format(res.status_code)
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
