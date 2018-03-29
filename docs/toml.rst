.. _toml:

toml
====

python lib for TOML

`<http://github.com/uiri/toml>`_

install
-------

install from pypi::

    $ pip install toml

usage
-----

import::

    import toml

function load::

    # toml to dict from toml file.
    dict_data = load(f, _dict=dict)

function loads::

    # toml to dict
    toml_dict = loads(s, _dict=dict)

function dump::

    # o to toml and write to f.
    dump(o, f)

function dumps::

    # o to toml
    toml_data = dumps(o)

