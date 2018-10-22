from super_devops.http.requests_wrapper import BaseRequests


class BaseGrafana(object):
    def __init__(self):
        pass

    def get_a_single_data_source_by_name(self):
        pass

    def create_data_source(self):
        pass

    def update_an_existing_data_source(self):
        pass

    def delete_an_existing_data_source_by_name(self):
        pass

    def create_or_update_dashboard(self):
        try:
            timestamp = Utils.timestamp()
            url = urlparse.urljoin(dashboard_url, "/api/dashboards/db")
            payload = json.dumps({
                "dashboard": dashboard,
                "folderId": 0,
                "overwrite": True,
                "message": "commit on {}".format(timestamp)
            })
            with BaseRequests(
                username=self.dashboard_username,
                password=self.dashboard_password,
                domain=None
            ) as req:
                res = req.post(
                    url, data=payload, json=None,
                    **{
                        'headers': self.headers,
                        'timeout': 60,
                        'verify': False
                    }
                )
                logger.debug(
                    "Grafana create or update dashboard res: {}".format(
                        res.content)
                )
            if res.status_code == 200:
                logger.info(
                    "Grafana create/update dashboard ({}) succeed.".format(
                        dashboard.get("title")
                    )
                )
                return True
            else:
                logger.error(
                    "Grafana create/update dashboard ({}) failed.".format(
                        dashboard.get("title")
                    )
                )
                return False
        except Exception as e:
            raise RuntimeError(
                "Grafana create/Update dashboard ({}) failed: {}".format(
                    dashboard.get("title"), e.message
                )
            )