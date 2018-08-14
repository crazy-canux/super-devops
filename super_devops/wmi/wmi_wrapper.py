import logging
import subprocess
import csv

logger = logging.getLogger(__name__)


class BaseWMI(object):

    def __init__(self, host, domain, username, password, **kwargs):

        self.host = host
        self.domain = domain
        self.username = username
        self.password = password
        self.kwargs = kwargs if kwargs else {}
        self.namespace = kwargs.get("namespace", r"root\cimv2")
        self.delimiter = kwargs.get("delimiter", r"|")

    def __enter__(self):
        logger.debug("BaseWMI.__enter__(): succeed.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("BaseWMI.__exit__(): succeed.")

    def query(self, wql):
        try:
            cmd = [
                'wmic',
                '-U',
                self.domain + '\\' + self.username + '%' + self.password,
                '//' + self.host,
                '--namespace',
                self.namespace,
                '--delimiter',
                self.delimiter,
                wql
            ]
            logger.debug("cmd: {}".format(cmd))
            __output = subprocess.check_output(cmd)
            logger.debug("output: {}".format(__output))
            __wmi_output = __output.splitlines()[1:]
            __result = csv.DictReader(__wmi_output, delimiter='|')
            logger.debug("result: {}".format(__result))
        except subprocess.CalledProcessError as e:
            raise e
        except Exception as e:
            raise e
        else:
            return list(__result)
