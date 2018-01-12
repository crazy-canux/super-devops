import logging
import argparse


logger = logging.getLogger(__name__)


class BaseNagios(object):
    def __init__(
            self,
            prog='nagios',
            description='Nagios Plugins',
            epilog='Nagios Plugins Command Line Options',
            version='0.0.1'
    ):
        logger.debug("Init BaseNagios.")

        self.prog = prog
        self.description = description
        self.epilog = epilog
        self.version = version

        # Init output data.
        self.nagios_output = ""
        self.shortoutput = ""
        self.perfdata = []
        self.longoutput = []

        # Init the argument
        self.__define_options()
        self.define_sub_options()
        self.__parse_options()

    def __define_options(self):
        self.parser = argparse.ArgumentParser(
            prog=self.prog,
            description=self.description,
            epilog=self.epilog,
            add_help=True
        )
        self.basic_parser = self.parser.add_argument_group(
            "Basic Options."
        )
        self.basic_parser.add_argument(
            '-D', '--debug',
            action='store_true',
            required=False,
            help='Debug mode.',
            dest='debug'
        )
        self.basic_parser.add_argument(
            '-V', '--version',
            action='version',
            version='%(prog)s {}'.format(self.version)
        )

    def define_sub_options(self):
        self.plugin_parser = self.parser.add_argument_group(
            "Basic Plugin Options"
        )
        self.plugin_parser.add_argument(
            "-H", "--host",
            default='127.0.0.1',
            required=True,
            help="Host IP address or DNS",
            dest="host"
        )
        self.plugin_parser.add_argument(
            "-u", "--username",
            default=None,
            required=False,
            help="Username",
            dest="username"
        )
        self.plugin_parser.add_argument(
            "-p", "--password",
            default=None,
            required=False,
            help="Password",
            dest="password"
        )
        self.plugin_parser.add_argument(
            '-d', '--domain',
            default=None,
            required=False,
            help='Domain',
            dest='domain'
        )

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
