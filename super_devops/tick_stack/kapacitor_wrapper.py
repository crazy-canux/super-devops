import urlparse
import logging
import json

from super_devops.http.requests_wrapper import BaseRequests

logger = logging.getLogger(__name__)


class BaseKapacitor(object):
    def __init__(
            self, kapacitor_url="http://localhost:9092/",
            username=None, password=None, domain=None
    ):
        self.kapacitor_url = kapacitor_url
        self.username = username
        self.password = password
        self.domain = domain

        self.base_url = urlparse.urljoin(
            self.kapacitor_url, "/kapacitor/v1"
        )

    def set_default_influxdb(
            self, influxdb_url="http://localhost:8086",
            default=True, enabled=True,
            username="", password=""
    ):
        try:
            url = self.base_url + "/config/influxdb/localhost"
            logger.debug("url: {}".format(url))
            payload = json.dumps({
                "set": {
                    "default": default,
                    "enabled": enabled,
                    "username": username,
                    "password": password,
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
            if res.status_code in [204, 200]:
                logger.info(
                    "Config default influxdb(localhost) for kapacitor succeed."
                )
                return True
            else:
                logger.error(
                    "Config default influxdb(localhost) for kapacitor failed."
                )
                return False
        except Exception:
            raise

    def __set_smtp(self, option):
        try:
            url = self.base_url + "/config/smtp/"
            logger.debug("url: {}".format(url))
            payload = json.dumps({
                "set": option
            })
            with BaseRequests(
                    username=self.username, password=self.password,
                    domain=self.domain
            ) as req:
                res = req.post(url, data=payload)
                logger.debug(
                    "Set smtp for kapacitor res: {}".format(res.content)
                )
                logger.debug(
                    "Set smtp for kapacitor status_code: {}".format(res.status_code)
                )
            if res.status_code in [200, 204]:
                logger.debug(
                    "Set smtp for kapacitor succeed."
                )
                return True
            else:
                logger.debug(
                    "Set smtp for kapacitor failed."
                )
                return False
        except Exception:
            raise

    def enable_smtp(
            self, host="localhost", port=25,
            frm="mail.super-devops.com", to=None,
            username="", password="", no_verify=True, idle_timeout="30s",
            global_enable=True, state_changes_only=False
    ):
        try:
            option = {
                "enabled": True,
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
            return self.__set_smtp(option)
        except Exception:
            raise

    def __get_smtp(self):
        try:
            url = self.base_url + "/config/smtp/"
            logger.debug("url: {}".format(url))
            with BaseRequests(
                username=self.username, password=self.password,
                domain=self.domain
            ) as req:
                res = req.get(url)
                logger.debug(
                    "Get smtp for kapacitor res: {}".format(res.content)
                )
                logger.debug(
                    "Get smtp for kapacitor status_code: {}".format(res.status_code)
                )
            if res.status_code == 200:
                logger.debug(
                    "Get smtp for kapacitor succeed."
                )
                option = json.loads(res.content).get("options")
                logger.debug("option: {}".format(option))
                return option
            else:
                logger.debug(
                    "Get smtp for kapacitor failed."
                )
                return False
        except Exception:
            raise

    def disable_smtp(self):
        try:
            option = self.__get_smtp()
            if isinstance(option, dict):
                option.pop("password")
                option["enabled"] = False
                if not option["to"]:
                    option["to"] = []
                return self.__set_smtp(option)
            else:
                return False
        except Exception:
            raise

    # TODO
    def get_all_tasks(self):
        """Only enabled tasks can be listed"""
        try:
            url = self.base_url + "/tasks"
        except Exception:
            raise

    def get_all_topics(self):
        try:
            url = self.base_url + "/alerts/topics"
            with BaseRequests(
                username=self.username, password=self.password,
                domain=self.domain
            ) as req:
                res = req.get(url)
                logger.debug(
                    "Get topics for kapacitor res: {}".format(res.content)
                )
                logger.debug(
                    "Get topics for kapacitor status_code: {}".format(
                        res.status_code)
                )
            if res.status_code == 200:
                logger.debug(
                    "Get topics for kapacitor succeed."
                )
                topics_list = json.loads(res.content).get("topics")
                topics = [
                    str(topic.get("id"))
                    for topic in topics_list
                    if not str(topic.get("id")).startswith("main")
                ]
                logger.debug("topics: {}".format(topics))
                return topics
            else:
                logger.debug(
                    "Get topics for kapacitor failed."
                )
                return False
        except Exception:
            raise

    def get_all_events(self, topic):
        try:
            url = self.base_url + "/alerts/topics/{}/events".format(topic)
        except Exception:
            raise

    def get_event(self, topic, event):
        try:
            url = self.base_url + "/alerts/topics/{}/events/{}".format(topic,
                                                                       event)
        except Exception:
            raise
