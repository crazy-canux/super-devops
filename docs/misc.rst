.. _misc:

colorama
========

Simple cross-platform colored terminal text in Python.

`<https://github.com/tartley/colorama>`_.

install
-------

install from pypi::

    $ pip install colorama

usage
-----

import::

    from colorama import Fore, Back, Style, init

functions::

    init()

data::

    Fore
    Back
    Style

examples::

    init()
    print Fore.RED + 'show red' + Fore.RESET # 字体颜色
    print Back.CYAN + 'show cyan in background' + Back.RESET # 背景颜色

decorator
=========

`<https://github.com/micheles/decorator>`_.o

install
-------

install from pypi::

    $ pip install decorator

usage
-----

enum
====

`<https://pypi.python.org/pypi/enum/0.4.6>`_.

install
-------

install from pypi::

    $ pip install enum

usage
-----

import::

    from enum import Enum, IntEnum

classes Enum::

    Enum

functions::

    unique(enumeration)

examples::

    clas Dataset(str, Enum):
        FIRST = 'one'
        SECOND = 'second'

    Dataset.FIRST.name # 'FIRST'
    Dataset.FIRST.value # 'one'
    Dataset('one') # Dataset.FIRST
    'one' in [Dataset.FIRST, Dataset.SECOND]
    'one' == Dataset.FIRST


