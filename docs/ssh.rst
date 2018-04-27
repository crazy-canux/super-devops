.. _ssh:

paramiko
========

`<https://github.com/paramiko/paramiko/>`_.

paramiko依赖pycrypto

install
-------

install from pypi::

    $ pip install paramiko

usage
-----

import::

    import paramiko

class SSHClient::

    client = paramiko.SSHClient()
    # methods:
    # timeout=None表示不会超时
    load_system_host_keys(filename=None)
    load_host_keys(filename)
    get_host_keys()
    set_missing_host_key_policy(policy)
    # paramiko.client.AutoAddPolicy() # 首次连接不用输入yes/no交互
    # paramiko.client.RejectPolicy()
    # paramiko.client.WarningPolicy()
    save_host_keys(self, filename)
    connect(hostname, port=22, username=None, password=None, pkey=None, key_filename=None, timeout=None, allow_agent=True, look_for_keys=True, compress=False, sock=None) # 支持连接本机
    # 查找Authentication顺序：
    # 1. pkey or key_filename
    # 2. allow_agent
    # 3. look_for_keys
    # 4. username/password
    stdin, stdout, stderr = exec_command(command, bufsize=-1, timeout=None, get_pty=False) # 返回三个ChannelFile类型的对象
    # get_pty可用于执行sudo命令输入密码，stdin.write(password + '\n'), stdin.flush()
    # stdin -> paramiko.ChannelFile
    # output = stdout.readlines() -> list
    # error = stderr.readlines() -> list
    invoke_shell(self, term='vt100', width=80, height=24, width_pixels=0, height_pixels=0)
    open_sftp(self)
    set_log_channel(self, name)
    get_transport() # return a Transport
    close(self)

class Transport::

    connect(self, hostkey=None, username='', password=None, pkey=None)
    cancel_port_forward(self, address, port)
    close(self)
    open_channel(self, kind, dest_addr=None, src_addr=None)  # Request channel to the server
    open_session(self) # alias of open_channel, return Channel
    run(self)
    send_ignore(self, bytes=None)
    start_client(self, event=None)
    start_server(self, event=None, server=None)
    stop_thread(self)
    use_compression(self, compress=True)

class Channel::

    close()
    exec_command(command)
    exit_status_ready(self)
    invoke_shell(self)
    invoke_subsystem(self, subsystem)
    makefile(self, *params)
    makefile_stderr(self, *params)
    recv(self, nbytes)
    recv_exit_status(self) # get command return code.
    recv_ready(self)
    recv_stderr(self, nbytes)
    recv_stderr_ready(self)
    send(self, s)
    send_exit_status(self, status)
    send_ready(self)
    send_stderr(self, s)
    sendall(self, s)
    sendall_stderr(self, s)
    settimeout(self, timeout)
    shutdown(self, how)
    shutdown_read(self)
    shutdown_write(self)

class ChannelFile::

    ChannelFile(BufferedFile)
    # methods
    read(size=None) # 读size字节，默认整个文件
    readline(size=None) # 读下一行
    readlines(sizehint=None) # 读所有行，返回list
    write(data)
    writelines(sequence)
    flush()
    close()

Issue::

    1. how to start/restart a process in paramiko
    sudo bash -c
    "nohup service <service> start/restart > /dev/null 2>&1 &" && sleep 5
