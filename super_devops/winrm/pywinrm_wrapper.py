import logging

import winrm


logger = logging.getLogger(__name__)
logging.getLogger('winrm').setLevel(logging.WARNING)


class BaseWinRM(object):

    def __init__(
            self, host, domain, username, password, **kwargs
    ):
        self.host = host
        self.domain = domain
        self.username = username
        self.password = password
        self.kwargs = kwargs

        # self.transport = kwargs.get('transport', 'plaintext')
        # self.realm = kwargs.get('realm', None)
        # self.service = kwargs.get("keytab", None)
        # self.keytab = kwargs.get("keytab", None)
        # self.ca_trust_path = kwargs.get("ca_trust_path", None)
        # self.cert_pem = kwargs.get("cert_pem", None)
        # self.cert_key_pem = kwargs.get("cert_key_pem", None)
        # self.server_cert_validation = kwargs.get(
        #     "server_cert_validation",
        #     u'validate'
        # )
        # self.kerberos_delegation = kwargs.get("kerberos_delegation", False)
        # self.read_timeout_sec = kwargs.get("read_timeout_sec", 30)
        # self.operation_timeout_sec = kwargs.get("operation_timeout_sec", 20)
        # self.kerberos_hostname_override = kwargs.get(
        #     "kerberos_hostname_override", None
        # )

        self.session = None

    def __enter__(self):
        self.session = winrm.Session(
            target=self.host,
            auth=(self.domain + '\\' + self.username, self.password),
            **self.kwargs
        )
        logger.debug("BaseWinRM.__enter__(): succeed.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("BaseWinRM.__exit__(): succeed.")

    def run_cmd(self, query):
        try:
            if query.split(",")[1:]:
                cmd = str(query.split(",")[0])
                args = query.split(",")[1:]
                __result = self.session.run_cmd(cmd, args)
            else:
                cmd = str(query)
                __result = self.session.run_cmd(cmd)
            logger.debug("cmd: {}".format(cmd))
            __return_code = __result.status_code
            logger.debug("Return code: {}".format(__return_code))
            __error = __result.std_err
            logger.debug("Error: {}".format(__error))
            __output = __result.std_out
            logger.debug("Output: {}".format(__output))
        except Exception as e:
            raise e
        else:
            if __error:
                logger.error("Run CMD error: {}".format(__error))
                return None
            else:
                return __output

    def run_ps(self, query):
        try:
            logger.debug("powershell: {}".format(query))
            __result = self.session.run_ps(query)
            __return_code = __result.status_code
            logger.debug("Return code: {}".format(__return_code))
            __error = __result.std_err
            logger.debug("Error: {}".format(__error))
            __output = __result.std_out
            logger.debug("Output: {}".format(__output))
        except Exception as e:
            raise e
        else:
            if __error:
                logger.error("Run PS error: {}".format(__error))
                return None
            else:
                return __output
