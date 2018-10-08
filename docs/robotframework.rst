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

run::

    # 调用该接口在程序里实现robot命令
    run(*tests, **options)
    # *tests是robot文件
    # **options包括所有robot命令的选项，另外还可以有stdout, stderr

    run_cli(arguments, exit=True)

rebot::

    rebot(*outputs, **options)

    rebot_cli(arguments, exit=True)

errors::

    from robot.errors import ExecutionFailed
    # raise this exception in keyword and set continue_on_failure to True
    # can keep going in the same case.
    raise ExecutionFailed(message=message, continue_on_failure=True)

api.logger::

    from robot.api import logger
    # robot的内置日志系统, 除了info可以同时选择输出到console,其它都是输出到logfile.
    logger.console(msg, newline=True, stream='stdout')
    logger.write(msg, level='INFO', html=False)
    logger.error(message, html=False) # 40
    logger.warn(message, html=False) # 30
    logger.info(message, html=False, also_console=False) # 一般用来打印case的执行情况． 20
    logger.debug(message, html=False) # 默认不打印 10
    logger.trace(message, html=False) # 默认不打印 0

api.deco::

    from robot.api.deco import keyword
    # 通过装饰器指定关键字名字和标签
    keyword(name=None, tags=())
    @keyword(name="the keyword name", tags=(tag1, tag2))
    def shortname():
        ...

api.TestData::

    from robot.api import TestData
    from robot.parsing.modle import TestData
    TestData(parent=None, source=None, include_suites=None,warn_on_skipped=False, extensions=None)
    # return model.TestCaseFile or model.TestDataDirectory
    testsuite = TestData(source="your.robot")


api.TestSuite::

    from robot.api import TestSuite

api.SuiteVisitor::

    from robot.api import SuiteVisitor

api.ExecutionResult::

    from robot.api import ExecutionResult

api.ResultWriter::

    from robot.api import ResultWriter
