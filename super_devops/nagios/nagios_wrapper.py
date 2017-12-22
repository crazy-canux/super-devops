import logging
import argparse


logger = logging.getLogger(__name__)

# TODO: refactor.


class Monitor(object):

    """Basic class for monitor.
    Nagios and tools based on nagios have the same status.
    All tools have the same output except check_mk.
        Services Status:
        0   OK
        1   Warning
        2   Critical
        3   Unknown
        Nagios Output(just support 4kb data):
        shortoutput - $SERVICEOUTPUT$
        -> The first line of text output from the last service check.
        perfdata - $SERVICEPERFDATA$
        -> Contain any performance data returned by the last service check.
        With format: | 'label'=value[UOM];[warn];[crit];[min];[max].
        longoutput - $LONGSERVICEOUTPUT$
        -> The full text output aside from the first line from the last service check.
        example:
        OK - shortoutput. |
        Longoutput line1
        Longoutput line2 |
        'perfdata'=value[UOM];[warn];[crit];[min];[max]
        Threshold:
        warning  warn_min:warn_max
        critical crit_min:crit_max
        warn_min < warn_max <= crit_min < crit_max
        10 == 0:10     => <0 or >10 alert
        10: == 10:æ   => <10 alert
        ~:10 == -æ:10 => >10 alert
        10:20          => <10 or >20 alert
        @10:20         => >=10 or <= 20 alert
    """

    def __init__(self):
        # Init the log.
        logging.basicConfig(format='[%(levelname)s] (%(module)s) %(message)s')
        self.logger = logging.getLogger("monitor")
        self.logger.setLevel(logging.INFO)

        # Init output data.
        self.nagios_output = ""
        self.shortoutput = ""
        self.perfdata = []
        self.longoutput = []

        # Init the argument
        self.__define_options()
        self.define_sub_options()
        self.__parse_options()

        # Init the logger
        if self.args.debug:
            self.logger.setLevel(logging.DEBUG)
        self.logger.debug("===== BEGIN DEBUG =====")
        self.logger.debug("Init Monitor")

        # End the debug.
        if self.__class__.__name__ == "Monitor":
            self.logger.debug("===== END DEBUG =====")

    def __define_options(self):
        self.parser = argparse.ArgumentParser(description="Plugin for Monitor.")
        self.parser.add_argument('-D', '--debug',
                                 action='store_true',
                                 required=False,
                                 help='Show debug informations.',
                                 dest='debug')

    def define_sub_options(self):
        """Define options for monitoring plugins.
        :param host: Monitoring Server IP address or Hostname.
        :type host: string.
        :param user: Monitoring Server User name.
        :type user: string.
        :param password: Monitoring Server User password.
        :type password: string.
        Rewrite your method and define your suparsers.
        Use subparsers.add_parser to create sub options for one function.
        """
        self.plugin_parser = self.parser.add_argument_group("Plugin Options",
                                                            "Options for all plugins.")
        self.plugin_parser.add_argument("-H", "--host",
                                        default='127.0.0.1',
                                        required=True,
                                        help="Host IP address or DNS",
                                        dest="host")
        self.plugin_parser.add_argument("-u", "--user",
                                        default=None,
                                        required=False,
                                        help="User name",
                                        dest="user")
        self.plugin_parser.add_argument("-p", "--password",
                                        default=None,
                                        required=False,
                                        help="User password",
                                        dest="password")

    def __parse_options(self):
        try:
            self.args = self.parser.parse_args()
        except Exception as e:
            self.unknown("Parser arguments error: {}".format(e))

    def output(self, substitute=None, long_output_limit=None):
        """Just for nagios output and tools based on nagios except check_mk.
        :param substitute: what you want to show in output.
        :type substitute: dict.
        :param long_output_limit: how many lines you want in output.
        :type long_output_limit: int.
        :return: return shortoutput + longoutput + perfdata.
        :rtype: string.
        """
        if not substitute:
            substitute = {}

        self.nagios_output += "{0}".format(self.shortoutput)
        if self.longoutput:
            self.nagios_output = self.nagios_output.rstrip("\n")
            self.nagios_output += " | \n{0}".format(
                "\n".join(self.longoutput[:long_output_limit]))
            if long_output_limit:
                self.nagios_output += "\n(...showing only first {0} lines, " \
                    "{1} elements remaining...)".format(
                        long_output_limit,
                        len(self.longoutput[long_output_limit:]))
        if self.perfdata:
            self.nagios_output = self.nagios_output.rstrip("\n")
            self.nagios_output += " | \n{0}".format(" ".join(self.perfdata))
        return self.nagios_output.format(**substitute)

    def __parse_threshold(self, threshold):
        """Get the min and max value from warning and critical threshold.
        :param threshold: warning or critical threshold.
        :type threshold: str.
        :return (min, max): min and max value.
        :rtype (min, max): tuple.
        """
        self.logger.debug("threshold: {}".format(threshold))
        if "@" in threshold:
            if ":" in threshold:
                return threshold.split("@")[1].split(":")[0], threshold.split("@")[1].split(":")[1]
            else:
                return 0, threshold.split("@")[1]
        else:
            if ":" in threshold:
                return threshold.split(":")[0], threshold.split(":")[1]
            else:
                return 0, threshold

    def __compare_threshold(self, result, mode):
        """Use the result compare with threshold.
        :param result: the result.
        :type result: int.
        :param mode: warning or critical.
        :type mode: str.
        :return status: status.
        :rtype status: function.
        """
        status = self.ok
        if mode == "warn":
            __min, __max = self.__parse_threshold(self.args.warning)
            threshold = self.args.warning
            status = self.warning
        elif mode == "crit":
            __min, __max = self.__parse_threshold(self.args.critical)
            threshold = self.args.critical
            status = self.critical
        else:
            self.unknown("Unknown threshold mode.")
        if __min > __max:
            self.unknown("Min must < Max in threshold.")

        if "~" == __min:
            if "@" in threshold:
                if result <= __max:
                    show = status
            else:
                if result > __max:
                    show = status
        elif not __max:
            if "@" in threshold:
                if result >= __min:
                    show = status
            else:
                if result < __min:
                    show = status
        else:
            if "@" in self.args.warning:
                if __min <= result <= __max:
                    show = status
            else:
                if result < __min or result > __max:
                    show = status
        return show

    def threshold(self, result):
        """Just for nagios, and tools based on nagios, except check_mk.
        :param result: the result of the service.
        :type result: int.
        :return status: the status of this service.
        :rtype status: method.
        """
        status = self.__compare_threshold(result, 'warn')
        status = self.__compare_threshold(result, 'crit')
        return status

    def ok(self, msg):
        raise MonitorOk(msg)

    def warning(self, msg):
        raise MonitorWarning(msg)

    def critical(self, msg):
        raise MonitorCritical(msg)

    def unknown(self, msg):
        raise MonitorUnknown(msg)


class MonitorOk(Exception):

    def __init__(self, msg):
        print("OK - %s" % msg)
        raise SystemExit(0)


class MonitorWarning(Exception):

    def __init__(self, msg):
        print("WARNING - %s" % msg)
        raise SystemExit(1)


class MonitorCritical(Exception):

    def __init__(self, msg):
        print("CRITICAL - %s" % msg)
        raise SystemExit(2)


class MonitorUnknown(Exception):

    def __init__(self, msg):
        print("UNKNOWN - %s" % msg)
        raise SystemExit(3)
