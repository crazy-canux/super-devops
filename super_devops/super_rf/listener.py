from robot.api import logger


class Listener(object):

    """Customize listener for super-devops.

    The default method will be called before customized method,
    Which use the same name.
    """

    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        pass

    def start_suite(self, data, result):
        msg = "Start test suite {}({}) at {} in robot framework.".format(
            data, result.id, result.starttime
        )
        logger.info(msg, also_console=True)
        logger.info('-' * len(msg), also_console=True)

    def end_suite(self, data, result):
        msg = "End test suite {}({}) at {} in robot framework.".format(
            data, result.id, result.starttime
        )
        logger.info(msg, also_console=True)
        logger.info('-' * len(msg), also_console=True)

    def start_test(self, data, result):
        logger.info('', also_console=True)

    def end_test(self, test, result):
        logger.info('', also_console=True)

    def start_keyword(self, data, result):
        pass

    def end_keyword(self, data, result):
        pass

    def log_message(self, message):
        pass

    def message(self, message):
        pass

    def close(self):
        pass
