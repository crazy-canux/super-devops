import logging
import subprocess

logger = logging.getLogger(__name__)


def query(self, wql):
    """Connect by wmi and run wql."""
    try:
        self.__wql = ['wmic', '-U',
                      self.args.domain + '\\' + self.args.user + '%' + self.args.password,
                      '//' + self.args.host,
                      '--namespace', self.args.namespace,
                      '--delimiter', self.args.delimiter,
                      wql]
        self.logger.debug("wql: {}".format(self.__wql))
        self.__output = subprocess.check_output(self.__wql)
        self.logger.debug("output: {}".format(self.__output))
        self.logger.debug("wmi connect succeed.")
        self.__wmi_output = self.__output.splitlines()[1:]
        self.logger.debug("wmi_output: {}".format(self.__wmi_output))
        self.__csv_header = csv.DictReader(self.__wmi_output, delimiter='|')
        self.logger.debug("csv_header: {}".format(self.__csv_header))
        return list(self.__csv_header)
    except subprocess.CalledProcessError as e:
        self.unknown("Connect by wmi and run wql error: %s" % e)