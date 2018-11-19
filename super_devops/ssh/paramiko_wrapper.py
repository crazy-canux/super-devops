import logging

import paramiko
from paramiko.client import SSHClient
from paramiko.ssh_exception import SSHException


logger = logging.getLogger(__name__)
logging.getLogger('paramiko').setLevel(logging.WARNING)


class BaseParamiko(SSHClient):

    """Customize paramiko for super-devops.

    with BaseParamiko(hostname, port, username, password, timeout) as ssh:
        output = ssh.exec_command(command)

    with BaseParamiko(hostname, port, username, password, timeout) as ssh:
        outputs = ssh.exec_commands(commands)
    """

    def __init__(
            self,
            hostname,
            username,
            password,
            port=22,
            timeout=60,
            **kwargs
    ):
        super(BaseParamiko, self).__init__()
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout

        # self.pkey = kwargs.get('pkey')
        # self.key_filename = kwargs.get('key_filename')
        # self.allow_agent = kwargs.get('allow_agent')
        # self.look_for_keys = kwargs.get('look_for_keys')
        # self.compress = kwargs.get('compress')
        # self.sock = kwargs.get('sock')
        # self.gss_auth = kwargs.get('gss_auth')
        # self.gss_kex = kwargs.get('gss_kex')
        # self.gss_deleg_creds = kwargs.get('gss_deleg_creds')
        # self.gss_host = kwargs.get('gss_host')
        # self.banner_timeout = kwargs.get('banner_timeout')
        # self.auth_timeout = kwargs.get('auth_timeout')
        # self.gss_trust_dns = kwargs.get('gss_trust_dns')

        self.kwargs = kwargs

    def __enter__(self):
        self.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
        super(BaseParamiko, self).connect(
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            timeout=self.timeout,
            **self.kwargs
        )
        logger.debug("BaseParamiko.__enter__(): succeed.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        logger.debug("BaseParamiko.__exit__(): succeed.")

    def exec_command(
            self,
            command,
            timeout=60,
            get_pty=False,
            sudo_pw=None,
            bufsize=-1,
            environment=None
    ):
        """Customize exec_command for super-devops.

        :param command: a shell command.
        :type command: string.
        :returns output: return stdout, stderr, rc
        :type output: ([], [], int)
        """
        try:
            logger.debug("Command: {}".format(command))
            stdin, stdout, stderr = super(BaseParamiko, self).exec_command(
                command, bufsize, timeout, get_pty, environment
            )
            if get_pty:
                if not sudo_pw:
                    sudo_pw = self.password
                stdin.write(sudo_pw + '\n')
                stdin.flush()
                logger.debug('Enter sudo password succeed.')
        except SSHException as e:
            logger.error("exec_command failed: {}".format(e.message))
            raise e
        except Exception as e:
            logger.error("Unknown error: {}".format(e.message))
            raise e
        else:
            try:
                return_code = stdout.channel.recv_exit_status()
                logger.debug("return code: {}".format(return_code))
                output_msg_list = stdout.readlines()
                stdout.close()
                logger.debug("output: {}".format(output_msg_list))
                error_msg_list = stderr.readlines()
                stderr.close()
                logger.debug("error: {}".format(error_msg_list))
            except Exception as e:
                logger.error("Get command result failed.")
                raise e
            else:
                return output_msg_list, error_msg_list, return_code

    def exec_script(
            self, script,
            timeout=60,
            get_pty=False,
            sudo_pw=None,
            bufsize=-1,
            environment=None
    ):
        try:
            cmd = 'sudo bash -c "%s"' % script
            output, error, rc = self.exec_command(
                cmd, timeout=timeout, get_pty=get_pty
            )
        except Exception:
            raise
        else:
            return output, error, rc

    def start_deamon(self, service, daemon, timeout=300, step=1):
        try:
            shell = """
                nohup service %s start > /dev/null 2>&1 &
                sleep %s
                for i in {1..%s}
                do
                    pidof %s && exit 0
                    sleep %s
                done
                exit 127
                """ % (service, step, timeout, daemon, step)
            output, error, rc = self.exec_script(
                shell, get_pty=True, timeout=timeout
            )
        except Exception as e:
            raise RuntimeError(
                "Start {} failed: {}".format(service, e.message)
            )
        else:
            return output, error, rc

    def stop_deamon(self, service, daemon, timeout=300, step=1):
        try:
            shell = """
                nohup service %s stop > /dev/null 2 >&1 &
                sleep %s
                for i in {1..%s}
                do 
                    pidof %s || exit 0
                    sleep %s
                done
                exit 127
                """ % (service, step, timeout, daemon, step)
            output, error, rc = self.exec_script(
                shell, get_pty=True, timeout=timeout
            )
        except Exception as e:
            raise RuntimeError(
                "Stop {} failed: {}".format(service, e.message)
            )
        else:
            return output, error, rc

    def start_service(self, service, timeout=300, step=1):
        try:
            shell = """
                nohup service %s start > /dev/null 2>&1 &
                sleep %s
                for i in {1..%s}
                do
                    ps -ef | grep -v grep | grep %s && exit 0
                    sleep %s
                done
                exit 127
                """ % (service, step, timeout, service, step)
            output, error, rc = self.exec_script(
                shell, get_pty=True, timeout=timeout
            )
        except Exception as e:
            raise RuntimeError(
                "Start {} failed: {}".format(service, e.message)
            )
        else:
            return output, error, rc

    def stop_service(self, service, timeout=300, step=1):
        try:
            shell = """
                nohup service %s stop > /dev/null 2 >&1 &
                sleep %s
                for i in {1..%s}
                do 
                    ps -ef | grep -v grep | grep %s || exit 0
                    sleep %s
                done
                exit 127
                """ % (service, step, timeout, service, step)
            output, error, rc = self.exec_script(
                shell, get_pty=True, timeout=timeout
            )
        except Exception as e:
            raise RuntimeError(
                "Stop {} failed: {}".format(service, e.message)
            )
        else:
            return output, error, rc

    def install_package(self, name, version):
        try:
            cmd = """
            sudo apt-get install --yes --reinstall 
            --allow-unauthenticated 
            -o Dpkg::Options::="--force-confnew" {}={}
            """.format(name, version)
            output, error, rc = self.exec_command(cmd, get_pty=True)
        except Exception as e:
            raise RuntimeError(
                "Install package {}_{} failed: {}".format(name,
                                                          version,
                                                          e.message)
            )
        else:
            return output, error, rc
