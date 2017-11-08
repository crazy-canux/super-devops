import paramiko
from paramiko.client import SSHClient
from paramiko.ssh_exception import SSHException
from robot.api import logger


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
        self.kwargs = kwargs

    def __enter__(self):
        self.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
        self.__connect(
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

    def __connect(
            self,
            hostname,
            port,
            username,
            password,
            timeout,
            **kwargs
    ):
        """Customize connect for super-devops."""
        try:
            pkey = kwargs.get('pkey')
            key_filename = kwargs.get('key_filename')
            allow_agent = kwargs.get('allow_agent')
            look_for_keys = kwargs.get('look_for_keys')
            compress = kwargs.get('compress')
            sock = kwargs.get('sock')
            gss_auth = kwargs.get('gss_auth')
            gss_kex = kwargs.get('gss_kex')
            gss_deleg_creds = kwargs.get('gss_deleg_creds')
            gss_host = kwargs.get('gss_host')
            banner_timeout = kwargs.get('banner_timeout')
            auth_timeout = kwargs.get('auth_timeout')
            gss_trust_dns = kwargs.get('gss_trust_dns')

            super(BaseParamiko, self).connect(
                hostname, port, username, password, pkey, key_filename,
                timeout, allow_agent, look_for_keys, compress, sock, gss_auth,
                gss_kex, gss_deleg_creds, gss_host, banner_timeout,
                auth_timeout, gss_trust_dns
            )
        except SSHException as e:
            logger.error("SSH connect failed: {}".format(e.message))
            raise e
        except Exception as e:
            logger.error("Unknown error: {}".format(e.message))
            raise e
        else:
            logger.debug("hostname:port : {}:{}".format(hostname, port))
            logger.debug("username/password: {}/{}".format(username, password))

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
        :returns output: return stdout + stderr.
        :type output: list.
        """
        try:
            stdin, stdout, stderr = super(BaseParamiko, self).exec_command(
                command, bufsize, timeout, get_pty, environment
            )
            if get_pty:
                stdin.write(sudo_pw + '\n')
        except SSHException as e:
            logger.error("exec_command failed: {}".format(e.message))
            raise e
        except Exception as e:
            logger.error("Unknown error: {}".format(e.message))
            raise e
        else:
            output_msg = stdout.readlines()
            error_msg = stderr.readlines()
            logger.debug("stderr: {}".format(output_msg))
            logger.debug("stdout: {}".format(error_msg))
        finally:
            stdout.close()
            stderr.close()
        output = output_msg + error_msg
        return output

    def exec_commands(
            self,
            commands,
            timeout=60,
            get_pty=False,
            sudo_pw=None,
            bufsize=-1,
            environment=None
    ):
        """A new method to run more than one commands.

        :param commands: lots of shell commands.
        :type commands: tuple/list.
        :returns outputs: all output for all commands.
        :type outputs: lists in list, like [[], [], ...]
        """
        outputs = []
        for command in commands:
            output = self.exec_command(
                command, timeout, bufsize, get_pty, sudo_pw, environment
            )
            outputs.append(output)
        return outputs
