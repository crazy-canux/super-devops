from robot.api import logger


class Listener(object):

    """Customize listener for super-devops.

    The default method will be called before customized method,
    Which use the same name.
    """

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        pass

    def start_suite(self, name, attributes):
        msg = "Start test suite {}({}) at {} in robot framework.".format(
            name, attributes.get("id"), attributes.get("starttime")
        )
        logger.info(msg, also_console=True)
        logger.info('-' * len(msg), also_console=True)

    def end_suite(self, name, attributes):
        msg = "End test suite {}({}) at {} in robot framework.".format(
            name, attributes.get('id'), attributes.get('starttime')
        )
        logger.info(msg, also_console=True)
        logger.info('-' * len(msg), also_console=True)

    def start_test(self, name, attributes):
        logger.info('', also_console=True)

    def end_test(self, name, attributes):
        pass

    def close(self):
        pass
