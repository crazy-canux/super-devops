.. _winrm:

pywinrm
=======


`<https://github.com/diyan/pywinrm>`_

install
-------

使用basic, certificate和NTLM::

    $ pip install pywinrm

使用kerberos需要安装::

    $ sudo apt-get install libkrb5-dev
    $ pip install pywinrm[kerberos]

使用CredSSP需要安装::

    $ sudo apt-get install libssl-dev
    $ pip install pywinrm[credssp]

transport参数:

Basic and Certificate(plaintext) just support local user.

SSL will use Certificate when used cert_pem and cert_key_pem, or revert to Basic over https.

NTLM support both local user and domain user, auth = 'domain\user'

CredSSP support both local user and domain user and just use https, auth = 'domain\user'

Kerberos just support domain user, auth = 'user@domain'

usage
-----

import::

    import winrm

class Session::

    # Wrapper Protocol class.
    Session(target, auth, **kwargs)
    # methods:
    run_cmd(self, command, args=())
    run_ps(self, script)

    # domain 用户使用 ntlm
    s = winrm.Session('ip address', auth=('domain\user', 'password'), transport='ntlm', server_cert_validation='ignore')
    r = s.run_cmd('ipconfig', ['/all'])
    return_code = r.status_code
    output = r.std_out
    error = r.std_err

class Protocol::

    Protocol(endpoint, transport=u'plaintext', username=None, password=None, realm=None, service=None, keytab=None, ca_trust_path=None, cert_pem=None, cert_key_pem=None, server_cert_validation=u'validate', kerberos_delegation=False, read_timeout_sec=30, operation_timeout_sec=20, kerberos_hostname_override=None)
    # methods:
    open_shell(self, i_stream=u'stdin', o_stream=u'stdout stderr',working_directory=None, env_vars=None, noprofile=False, codepage=437,lifetime=None, idle_timeout=None)
    run_command(self, shell_id, command, arguments=(), console_mode_stdin=True,skip_cmd_shell=False)
    get_command_output(self, shell_id, command_id)
    send_message(self, message)
    cleanup_command(self, shell_id, command_id)
    close_shell(self, shell_id)

    # domain 用户使用 ntlm
    p = winrm.Protocol(endpoint='http://127.0.0.1:5985/wsman', transport='ntlm', username=r'DOMAIN\user', password='password',server_cert_validation='ignore')
    shell_id = p.open_shell()
    command_id = p.run_command(shell_id, 'ipconfig', ['/all'])
    std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
    p.cleanup_command(shell_id, command_id)
    p.close_shell(shell_id)
