import logging
import time
import json

import urllib.parse as urlparse

from .requests_wrapper import BaseRequests

logger = logging.getLogger(__name__)


class BaseLoki(object):
    """
    *time: unix epoch in nanoseconds
    """
    def __init__(
            self, loki_url="http://localhost:3100/",
            username=None, password=None
    ):
        self.loki_url = loki_url
        self.username = username
        self.password = password

        self.header = {
            'Content-Type': 'application/json'
        }

    def query_range(self, query, start=None, end=None, step=None, limit=None, direction="backward"):
        """

        :param query:
        :param start: one hour ago(default).
        :param end: now(default).
        :param step: start-end(default).
        :param limit: 5000 (default).
        :param direction: backward(default), forward.
        :return:
        """
        try:
            url = urlparse.urljoin(
                self.loki_url, "/loki/api/v1/query_range"
            )
            payload = {
                "query": query,
                "start": start,
                "end": end,
                "step": step,
                "limit": limit,
                "direction": direction
            }
            with BaseRequests(
                    username=self.username,
                    password=self.password
            ) as req:
                res = req.get(
                    url, params=payload,
                    **{
                        'headers': self.header,
                        'timeout': 60
                    }
                )
                logger.debug("resp: {}".format(res.content))
                # logger.debug("status_code: {}".format(res.status_code))
            if res.status_code == 200:
                return res.content
            else:
                logger.error("query-range failed: {}".format(res.reason))
                return ""
        except Exception:
            raise

    def query(self, query, ts=None, limit="1000", direction="backward"):
        """

        :param query:
        :param limit: 1000 (default).
        :param time: epoch time (default now).
        :param direction: backward(default, forward.
        :return:
        """
        try:
            url = urlparse.urljoin(
                self.loki_url, "/loki/api/v1/query"
            )
            print(url)
            payload = {
                "query": query,
                "limit": limit,
                "direction": direction
            }
            # "time": ts if ts else time.time(),
            with BaseRequests(
                    username=self.username,
                    password=self.password
            ) as req:
                res = req.get(
                    url, params=payload,
                    **{
                        'headers': self.header,
                        'timeout': 60
                    }
                )
                logger.debug("resp: {}".format(res.content))
                logger.debug("status_code: {}".format(res.status_code))
            if res.status_code == 200:
                return res.content
            else:
                logger.error("query failed: {}".format(res.reason))
                return ""
        except Exception:
            raise

    def tail(self, query, start=None, delay_for=0, limit="1000"):
        """

        :param query:
        :param start: one hour ago (default)
        :param delay_for: 0 (default), <= 5
        :param limit: 1000
        :return:
        """
        try:
            url = urlparse.urljoin(
                self.loki_url, "/loki/api/v1/tail"
            )
            print(url)
            payload = {
                "query": query,
                "start": start,
                "delay_for": delay_for,
                "limit": limit
            }
            # "time": ts if ts else time.time(),
            with BaseRequests(
                    username=self.username,
                    password=self.password
            ) as req:
                res = req.get(
                    url, params=payload,
                    **{
                        'headers': self.header,
                        'timeout': 60
                    }
                )
                logger.debug("resp: {}".format(res.content))
                logger.debug("status_code: {}".format(res.status_code))
            if res.status_code == 200:
                return res.content
            else:
                logger.error("tail failed: {}".format(res.reason))
                return ""
        except Exception:
            raise

    def push(self, stream, message):
        try:
            now = "%.9f" % time.time()
            n_now = now.replace(".", "")
            url = urlparse.urljoin(
                self.loki_url, "/loki/api/v1/push"
            )
            streams = {
                "streams": [
                    {
                        "stream": stream,
                        "values": [
                            [n_now, message]
                        ]
                    }
                ]
            }
            payload = json.dumps(streams)
            with BaseRequests(
                    username=self.username,
                    password=self.password
            ) as req:
                res = req.post(
                    url, data=payload, json=None,
                    **{
                        'headers': self.header,
                        'timeout': 60
                    }
                )
                # logger.debug("resp: {}".format(res.content))
                # logger.debug("status_code: {}".format(res.status_code))
                logger.debug("Log to push: ".format(message))
            if res.status_code == 204:
                return True
            else:
                logger.error("push failed: {}".format(res.reason))
                return False
        except Exception:
            raise
