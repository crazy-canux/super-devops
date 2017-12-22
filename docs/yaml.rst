.. _yaml:

pyyaml
======

YAML parser and emitter for Python

`<http://pyyaml.org/wiki/PyYAML>`_

install
-------

install from pypi::

    $ pip install pyyaml

usage
-----

import::

    import yaml

class YAMLObject::

    YAMLObject

    # methods:
    from_yaml(cls, loader, node)
    to_yaml(cls, dumper, data)

class YAMLError::

    YAMLError

functions::

    add_constructor(tag, constructor, Loader=<class 'yaml.loader.Loader'>)

    dump(data, stream=None, Dumper=<class 'yaml.dumper.Dumper'>, **kwds)
    # dump(data, open(file, 'w')),　序列化python对象data到stream,一般是一个文件，如果stream=None, 返回生成的字符串．
    safe_dump(data, stream=None, **kwds) # 序列化最基本的tag
    dump_all(documents, stream=None, Dumper=<class 'yaml.dumper.Dumper'>, default_style=None, default_flow_style=None, canonical=None, indent=None, width=None, allow_unicode=None, line_break=None, encoding='utf-8', explicit_start=None, explicit_end=None, version=None, tags=None)

    load(stream, Loader=<class 'yaml.loader.Loader'>)
    # data = load(open(file, 'r')), 从stream中解析第一个yaml文档．
    safe_load(stream) # 解析最基本的tag
    load_all(stream, Loader=<class 'yaml.loader.Loader'>)


