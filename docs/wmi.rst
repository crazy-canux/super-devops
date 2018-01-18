.. _wmi:

wmi
===

install
-------

Windows安装pywin32和wmi两个包,可以访问wmi::

    `<https://sourceforge.net/projects/pywin32/?source=navbar>`_
    `<http://timgolden.me.uk/python/wmi/index.html>`_

linux需要先安装wmic命令,通过subprocess/sh远程执行wmic命令::

    # subprocess is PSL
    $ pip install sh

usage
-----

import::

    # windows:
    import wmi

    # linux:
    import subprocess
    # OR
    from sh import wmic

windows::

    c = wmi.WMI()
    c.<wmi class/wmi provider>

linux::

    command = ['wmic', '-U', domain\\user%password, //host, wql]
    wmi_output = subprocess.check_output(command)

    arguments = ['-U', domain\\user%password, //host, wql]
    output = sh.wmic(arguments)
