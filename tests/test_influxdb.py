import unittest
import json
import urlparse
import time

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from super_devops.ssh.paramiko_wrapper import BaseParamiko
from super_devops.http.requests_wrapper import BaseRequests


def start_service(node, username, password, service, daemon):
    """influxd, grafana-server, telegraf, kapacitord"""
    try:
        with BaseParamiko(
                hostname=node, username=username, password=password
        ) as ssh:
            kill_cmd = "sudo pkill -ef {}".format(service)
            out, err, rtc = ssh.exec_command(
                kill_cmd, get_pty=True, sudo_pw=password
            )
            print("kill {} output: {}".format(service, out))
            print("kill {} error: {}".format(service, err))

            shell = """
            nohup service %s start > /dev/null 2>&1 &
            sleep 1
            for i in {1..60}
            do
                pidof %s && exit 0
                sleep 1
            done
            exit 127
            """ % (service, daemon)
            cmd = 'sudo bash -c "%s"' % shell
            output, error, rc = ssh.exec_command(
                cmd, get_pty=True, sudo_pw=password
            )
            print("restart {} output: {}".format(service, output))
            print("restart {} error: {}".format(service, error))
    except Exception as e:
        raise RuntimeError(
            "Restart {} on {} failed: {}".format(service, node, e.message)
        )


def show_database():
    try:
        url = urlparse.urljoin("http://127.0.0.1:8086", "/query")
        payload = {
            "q": "SHOW DATABASES"
        }
        with BaseRequests(
                username=None,
                password=None,
                domain=None
        ) as req:
            res = req.get(
                url, params=payload,
                **{
                    'headers': {'Content-Type': 'application/json'},
                    'timeout': 60,
                    'verify': False
                }
            )
            print("show database res: {}".format(res.content))
        if res.status_code == 200:
            db_lst = json.loads(res.content).get(
                "results")[0].get("series")[0].get("values")
            print("db list: {}".format(db_lst))
        else:
            print("Show influxdb database failed")
    except Exception as e:
        raise RuntimeError(
            "Show influxdb databases failed: {}".format(e.message)
        )


if __name__ == "__main__":
    start_service('127.0.0.1', 'canux', 'canux', 'influxdb', 'influxd')
    # time.sleep(5)
    # show_database()
