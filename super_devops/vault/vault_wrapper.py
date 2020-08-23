import logging
import json
from urllib.parse import urljoin

from .requests_wrapper import BaseRequests

logger = logging.getLogger()


class BaseVault(object):
    def __init__(self, server="https://127.0.0.1:8200/", version="v1"):
        super(BaseVault, self).__init__()
        self.base = urljoin(server, version) + "/"

    def health(self, kind="init"):
        try:
            url = urljoin(self.base, "sys/health")
            with BaseRequests() as req:
                resp = req.get(url)
            if resp.status_code == 200:
                logger.debug("initialized, unsealed and active.")
                return True
            elif resp.status_code == 503:
                logger.debug("initialized but sealed.")
                if kind.lower() == "init":
                    return True
                else:
                    return False
            elif resp.status_code == 501:
                logger.debug("not initialized.")
                return False
            else:
                return False
        except Exception:
            raise

    def seal_status(self):
        try:
            url = urljoin(self.base, "sys/seal-status")
            with BaseRequests() as req:
                resp = req.get(url)
            if resp.status_code == 200:
                if resp.json()["sealed"]:
                    return True
                else:
                    return False
            else:
                raise Exception("get seal status failed.")
        except Exception:
            raise

    def init(self):
        try:
            url = urljoin(self.base, "sys/init")
            payload = {
                "secret_shares": 5,
                "secret_threshold": 3,
            }
            with BaseRequests() as req:
                resp = req.put(url, data=json.dumps(payload))
            if resp.status_code == 200:
                return resp.json()
            else:
                raise Exception("vault init failed")
        except Exception:
            raise

    def unseal(self, key):
        try:
            url = urljoin(self.base, "sys/unseal")
            payload = {
                "key": key,
                "reset": False,
                "migrate": False
            }
            with BaseRequests() as req:
                resp = req.put(url, json.dumps(payload))
            if resp.status_code == 200:
                if resp.json()["sealed"]:
                    return False
                else:
                    return True
            else:
                raise Exception("vault unseal failed.")
        except Exception:
            raise

    def enable_kv2(self, token, path):
        try:
            url = urljoin(self.base, "sys/mounts/{}".format(path))
            headers = {
                "X-Vault-Token": token
            }
            payload = {
                "type": "kv",
                "description": "kv-2 secrets",
                "options": {
                    "version": "2"
                },
                "config": {
                    "default_lease_ttl": 0,
                    "max_lease_ttl": 0
                },
                "local": False,
                "seal_wrap": False,
                "external_entropy_access": False
            }
            with BaseRequests() as req:
                resp = req.post(url, data=json.dumps(payload), **{"headers": headers})
            if resp.status_code == 204:
                return True
            else:
                return False
        except Exception:
            raise

    def create_policy(self, token, name, path):
        try:
            url = urljoin(self.base, "sys/policy/{}".format(name))
            headers = {
                "X-Vault-Token": token
            }
            payload = {
                "policy": "path \"%s/*\" {\"capabilities\" = [\"create\", \"read\", \"update\", \"delete\", \"list\"]}" % path
            }
            with BaseRequests() as req:
                resp = req.put(url, data=json.dumps(payload), **{"headers": headers})
            if resp.status_code == 204:
                return True
            else:
                return False
        except Exception:
            raise

    def seal(self, token):
        try:
            url = urljoin(self.base, "sys/seal")
            headers = {
                "X-Vault-Token": token
            }
            with BaseRequests() as req:
                resp = req.put(url, **{"headers": headers})
            if resp.status_code == 200:
                return True
            else:
                return False
        except Exception:
            raise

    def get(self, token, engine, path):
        try:
            url = urljoin(self.base, "{}/data/{}".format(engine, path))
            headers = {
                "X-Vault-Token": token
            }
            with BaseRequests() as req:
                resp = req.get(url, **{"headers": headers})
            if resp.status_code == 200:
                return resp.json()["data"]["data"]
            else:
                return None
        except Exception:
            raise

    def put(self, token, engine, path, data):
        try:
            url = urljoin(self.base, "{}/data/{}".format(engine, path))
            payload = {
                "data": data
            }
            headers = {
                "X-Vault-Token": token
            }
            with BaseRequests() as req:
                resp = req.post(url, data=json.dumps(payload), **{"headers": headers})
            if resp.status_code == 200:
                return True
            else:
                return False
        except Exception:
            raise

    def delete(self, token, engine, path):
        try:
            url = urljoin(self.base, "{}/data/{}".format(engine, path))
            headers = {
                "X-Vault-Token": token
            }
            with BaseRequests() as req:
                resp = req.delete(url, **{"headers": headers})
            if resp.status_code == 200:
                return resp.json()["data"]["data"]
            else:
                return None
        except Exception:
            raise

