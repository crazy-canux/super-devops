.. _robotframework:

robotframework
==============

install
-------

install from pypi::

    $ pip install robotframework

usage
-----

import::

    import robot

functions::

    # 调用该接口在程序里实现robot命令
    run(*tests, **options)
    # *tests是robot文件
    # **options包括所有robot命令的选项，另外还可以有stdout, stderr

    run_cli(arguments, exit=True)

    rebot(*outputs, **options)

    rebot_cli(arguments, exit=True)

    from robot.api import logger
    # robot的内置日志系统, 除了info可以同时选择输出到console,其它都是输出到logfile.
    logger.console(msg, newline=True, stream='stdout')
    logger.write(msg, level='INFO', html=False)
    logger.error(message, html=False) # 40
    logger.warn(message, html=False) # 30
    logger.info(message, html=False, also_console=False) # 一般用来打印case的执行情况． 20
    logger.debug(message, html=False) # 默认不打印 10
    logger.trace(message, html=False) # 默认不打印 0

    from robot.api.deco import keyword
    # 通过装饰器指定关键字名字和标签
    keyword(name=None, tags=())
    @keyword(name="the keyword name", tags=(tag1, tag2))
    def shortname():
        ...

    from robot.parsing.modle import TestData
    TestData(parent=None, source=None, include_suites=None,warn_on_skipped=False, extensions=None)
    # return model.TestCaseFile or model.TestDataDirectory
    testsuite = TestData(source="your.robot")

    from robot.errors import ExecutionFailed
