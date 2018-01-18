import logging
import subprocess
import shlex
import csv

logger = logging.getLogger(__name__)

class BaseWMI(object):

    def __init__(self, host, domain, username, password, **kwargs):

        self.host = host
        self.domain = domain
        self.username = username
        self.password = password
        self.kwargs = kwargs if kwargs else {}
        self.namespace = kwargs.get("namespace", "root\cimv2")
        self.delimiter = kwargs.get("delimiter", "|")

    def __enter__(self):
        logger.debug("BaseWMI.__enter__(): succeed.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("BaseWMI.__exit__(): succeed.")

    def query(self, wql):
        cmd = 'wmic -U {domain}\\{username}%{password} //{host} ' \
              '--namespace {namesapce} --delimiter {delimiter} {wql}'.format(
            domain=self.domain,
            username=self.username,
            password=self.password,
            host=self.host,
            namesapce=self.namesapce,
            delimiter=self.delimiter,
            wql=wql
        )
        logger.debug("wql: {}".format(wql))
        __output = subprocess.check_output(shlex.split(cmd))
        logger.debug("output: {}".format(__output))
        __wmi_output = __output.splitlines()[1:]
        __result = csv.DictReader(__wmi_output, delimiter='|')
        self.logger.debug("result: {}".format(__result))
    except subprocess.CalledProcessError as e:
        raise e
    except Exception as e:
        raise e
    else:
        return list(__result)
