import urlparse
import json
import logging

from super_devops.http.requests_wrapper import BaseRequests
from super_devops.utils import Utils

logger = logging.getLogger(__name__)


class BaseGrafana(object):
    def __init__(
            self, grafana_url="http://localhost:3000",
            username=None, password=None, domain=None
    ):
        self.grafana_url = grafana_url
        self.username = username
        self.password = password
        self.domain = domain

        self.header = {'Content-Type': 'application/json'}

    def check_data_source_exist_by_name(self, name):
        try:
            url = urlparse.urljoin(
                self.grafana_url,
                "/api/datasources/name/{}".format(name)
            )
            with BaseRequests(
                    username=self.username,
                    password=self.password,
                    domain=self.domain
            ) as req:
                res = req.get(
                    url,
                    **{
                        'headers': self.header,
                        'timeout': 60,
                        'verify': False
                    }
                )
                logger.debug(
                    "Check data source exist by name res: {}".format(
                        res.content)
                )
            if res.status_code == 200:
                logger.info(
                    "Data source {} exist.".format(name)
                )
                return True
            else:
                if res.json().get("message") == "Data source not found":
                    logger.error("Data source {} not exist.".format(name))
                    return False
                else:
                    logger.error("Check data source by name failed.")
                    return False
        except Exception:
            raise

    def create_data_source_from_influxdb(
            self, name, influxdb_url, access="proxy", is_default=False,
            database=""
    ):
        try:
            url = urlparse.urljoin(self.grafana_url, "/api/datasources")
            payload = json.dumps({
                "name": name,
                "type": "influxdb",
                "url": influxdb_url,
                "database": database,
                "access": access,
                "isDefault": is_default
            })
            with BaseRequests(
                    username=self.username,
                    password=self.password,
                    domain=self.domain
            ) as req:
                res = req.post(
                    url, data=payload, json=None,
                    **{
                        'headers': self.header,
                        'timeout': 60,
                        'verify': False
                    }
                )
                logger.debug(
                    "Create data source from influxdb res: {}".format(
                        res.content)
                )
            if res.status_code == 200:
                logger.info(
                    "Create data source {} from influxdb succeed.".format(
                        name)
                )
                return True
            else:
                logger.error(
                    "Create data source {} from influxdb failed.".format(
                        name)
                )
                return False
        except Exception:
            raise

    def delete_an_existing_data_source_by_name(self, name):
        try:
            url = urlparse.urljoin(
                self.grafana_url,
                "/api/datasources/name/{}".format(name)
            )
            with BaseRequests(
                    username=self.username,
                    password=self.password,
                    domain=self.domain
            ) as req:
                res = req.delete(
                    url,
                    **{
                        'headers': self.header,
                        'timeout': 60,
                        'verify': False
                    }
                )
                logger.debug(
                    "Delete an existing data source by name res: {}".format(
                        res.content)
                )
            if res.status_code == 200:
                logger.info(
                    "Delete an existing data source {} by name succeed.".format(
                        name)
                )
                return True
            else:
                logger.error(
                    "Delete an existing data source {} by name failed.".format(
                        name)
                )
                return False
        except Exception:
            raise

    def create_or_update_dashboard(self, filename):
        try:
            with open(filename, 'r') as f:
                dashboard = json.load(f)
            timestamp = Utils.timestamp()
            url = urlparse.urljoin(self.grafana_url, "/api/dashboards/db")
            payload = json.dumps({
                "dashboard": dashboard,
                "folderId": 0,
                "overwrite": True,
                "message": "commit on {}".format(timestamp)
            })
            with BaseRequests(
                    username=self.username,
                    password=self.password,
                    domain=self.domain
            ) as req:
                res = req.post(
                    url, data=payload, json=None,
                    **{
                        'headers': self.header,
                        'timeout': 60,
                        'verify': False
                    }
                )
                logger.debug(
                    "Create or update dashboard res: {}".format(
                        res.content)
                )
            if res.status_code == 200:
                logger.info(
                    "Create or update dashboard {} succeed.".format(
                        dashboard.get("title")
                    )
                )
                return True
            else:
                logger.error(
                    "Create or update dashboard {} failed.".format(
                        dashboard.get("title")
                    )
                )
                return False
        except Exception:
            raise

    def update_current_user_prefs(self, theme="light", timezone="utc"):
        try:
            url = urlparse.urljoin(self.grafana_url, "/api/user/preferences")
            payload = json.dumps({
                "theme": theme,
                "homeDashboardId": 0,
                "timezone": timezone
            })
            with BaseRequests(
                username=self.username,
                password=self.password,
                domain=self.domain
            ) as req:
                res = req.put(url, data=payload)
                logger.debug(
                    "Update current user prefs: {}".format(res.content)
                )
            if res.status_code == 200:
                logger.info("Update current user prefs succeed.")
                return True
            else:
                logger.error("Update current user prefs failed.")
                return False
        except Exception:
            raise

    def create_new_global_user(self, name, email, password, login="test"):
        """Default is viewer"""
        try:
            url = urlparse.urljoin(self.grafana_url, "/api/admin/users")
            payload = json.dumps({
                "name": name,
                "email": email,
                "login": login if login else name,
                "password": password
            })
            with BaseRequests(
                username=self.username,
                password=self.password,
                domain=self.domain
            ) as req:
                res = req.post(url, data=payload)
                logger.debug(
                    "Create new global user: {}".format(res.content)
                )
            if res.status_code == 200:
                logger.info("Create new global user succeed.")
                return json.loads(res.content).get("id")
            else:
                logger.error("Create new global user failed.")
                return False
        except Exception:
            raise
