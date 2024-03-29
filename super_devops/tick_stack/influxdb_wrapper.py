import logging
import urllib.parse as urlparse
import json

from super_devops.super_http.requests_wrapper import BaseRequests

logger = logging.getLogger(__name__)


class BaseInfluxdb(object):
    def __init__(
            self, influxdb_url="http://localhost:8086/",
            username=None, password=None
    ):
        self.influxdb_url = influxdb_url
        self.username = username
        self.password = password

        self.header = {'Content-Type': 'application/json'}

        self.write_url = urlparse.urljoin(
            self.influxdb_url, "/write"
        )
        self.query_url = urlparse.urljoin(
            self.influxdb_url, "/query"
        )

    def check_database_exist(self, database):
        try:
            payload = {
                "q": "SHOW DATABASES"
            }
            with BaseRequests(
                    username=self.username,
                    password=self.password
            ) as req:
                res = req.get(
                    self.query_url, params=payload,
                    **{
                        'headers': self.header,
                        'timeout': 60,
                        'verify': False
                    }
                )
                logger.debug("show database res: {}".format(res.content))
            if res.status_code == 200:
                db_lst = json.loads(str(res.content, "utf-8")).get(
                    "results")[0].get("series")[0].get("values")
                logger.debug("db list: {}".format(db_lst))
                if db_lst and ([database] in db_lst):
                    logger.info(
                        "Database {} already exist".format(database)
                    )
                    return True
                else:
                    logger.warning(
                        "Database {} not exist.".format(database)
                    )
                    return False
            else:
                logger.error("Check database exist failed")
                return False
        except Exception:
            raise

    def create_database(self, database):
        try:
            payload = {
                "q": "CREATE DATABASE {}".format(database)
            }
            with BaseRequests(
                    username=self.username,
                    password=self.password
            ) as req:
                res = req.post(self.query_url, data=payload)
                logger.debug("Create database res: {}".format(res.content))
            if res.status_code == 200:
                logger.info(
                    "Create database {} succeed.".format(database)
                )
                return True
            else:
                logger.error(
                    "Create database {} failed.".format(database)
                )
                return False
        except Exception:
            raise

    def create_retention_policy(
            self, database, rp="autogen", duration="0s", replication=1,
            default=True
    ):
        try:
            if default:
                payload = {
                    "q": "CREATE RETENTION POLICY {} ON {} "
                         "DURATION {} REPLICATION {} DEFAULT".format(
                        rp, database, duration, replication)
                }
            else:
                payload = {
                    "q": "CREATE RETENTION POLICY {} ON {} "
                         "DURATION {} REPLICATION {}".format(
                        rp, database, duration, replication)
                }
            with BaseRequests(
                    username=self.username,
                    password=self.password
            ) as req:
                res = req.post(self.query_url, data=payload)
                logger.debug(
                    "Create retention policy res: {}".format(res.content)
                )
            if res.status_code == 200:
                logger.info(
                    "Create rp {} on {} succeed.".format(rp, database)
                )
                return True
            else:
                logger.error(
                    "Create rp {} on {} failed.".format(rp, database)
                )
                return False
        except Exception:
            raise

    def show(self, ifql):
        try:
            payload = {
                "q": ifql
            }
            with BaseRequests(
                    username=self.username,
                    password=self.password
            ) as req:
                res = req.get(
                    self.query_url, params=payload,
                    **{
                        'headers': self.header,
                        'timeout': 60,
                        'verify': False
                    }
                )
                logger.debug("show res: {}".format(res.content))
            if res.status_code == 200:
                return json.loads(str(res.content, "utf-8"))
            else:
                logger.error("show failed")
                return None
        except Exception:
            raise

    def query(self, db, ifql):
        try:
            url = urlparse.urljoin(
                self.influxdb_url, "/query?db={}".format(db)
            )
            payload = {
                "q": ifql,
                "epoch": "ms"
            }
            with BaseRequests(
                    username=self.username,
                    password=self.password
            ) as req:
                res = req.get(
                    url, params=payload,
                    **{
                        'headers': self.header,
                        'timeout': 60,
                        'verify': False
                    }
                )
                logger.debug("select res: {}".format(res.content))
            if res.status_code == 200:
                return json.loads(str(res.content, "utf-8"))
            else:
                logger.error("select failed.")
                return None
        except Exception:
            raise
