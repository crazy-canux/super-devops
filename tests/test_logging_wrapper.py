from super_devops.logging.logging_wrapper import BaseLogging


logger = BaseLogging(__name__).init_debug_and_info_logger(
    '/home/canux/Src/super-devops/tests/data/debug.log',
    '/home/canux/Src/super-devops/tests/data/info.log',
)


logger.debug("test debug")
logger.info("test info")
logger.warn("test warn")
