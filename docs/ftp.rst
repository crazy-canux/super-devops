.. _ftp:

ftplib
======

ftplib模块用来编写ftp客户端程序：

usage
-----

import::

    from ftplib import FTP

class FTP::

    FTP(self, host='', user='', passwd='', acct='', timeout=<object>)
    ftp = FTP()

    # methods
    connect(self, host='', port=0, timeout=-999)    连接到主机
    login(self, user='', passwd='', acct='')    登录
    acct(self, password)
    cwd(self, dirname)    更改工作路径

    dir(self, *args)    列出路径（文件也会输出）, 类似于LIST
    # 获取ftp一个路径下的文件和子目录
    data = []
    ftp.dir(path, data.append)

    nlst(self, *args)   列出给定路径的文件（目录也会输出）， 类似于NLST
    pwd(self) 返回当前工作路径
    size(self, filename) 获取文件大小
    delete(self, filename)
    getline(self)
    getmultiline(self)
    getresp(self)
    getwelcome(self)
    makepasv(self)
    makeport(self)
    mkd(self, dirname)
    ntransfercmd(self, cmd, rest=None)
    putcmd(self, line)
    putline(self, line)
    rename(self, fromname, toname)

    retrbinary(self, cmd, callback, blocksize=8192, rest=None)
    # 二进制下载文件
    # cmd: a RETR command, like "RETR filename"
    # 下载ftp服务器的文件
    f = open(filename, 'wb')
    ftp.retrbinary("RETR %s" filename, f.write)
    f.close()

    retrlines(self, cmd, callback=None)
    # 文本下载文件
    # cmd: a RETR, LIST, NLST, or MLSD command.

    rmd(self, dirname)
    sanitize(self, s)
    sendcmd(self, cmd)
    sendeprt(self, host, port)
    sendport(self, host, port)
    set_debuglevel(self, level)
    set_pasv(self, val)

    storbinary(self, cmd, fp, blocksize=8192, callback=None, rest=None)
    # 二进制上传文件

    storlines(self, cmd, fp, callback=None)
    # 文本上传文件

    transfercmd(self, cmd, rest=None)
    voidcmd(self, cmd)
    voidresp(self)
    close(self)    关闭连接
    quit(self) 退出并关闭连接

