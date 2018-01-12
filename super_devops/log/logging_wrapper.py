import logging

# TODO: if log file not exist, make it and grant access.


class BaseLogging(object):

    @staticmethod
    def init_logger(log_file):
        format = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
        logging.basicConfig(
            level=logging.DEBUG,
            format=format,
            filename=log_file,
            filemode='a'
        )
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(format)
        console.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(console)

    @staticmethod
    def init_2_logger(debug_file=None, info_file=None):
        format = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
        logging.basicConfig(
            level=logging.DEBUG,
            format=format,
            filename=debug_file,
            filemode='a'
        )
        formatter = logging.Formatter(format)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(console)

        web = logging.FileHandler(info_file, 'w')
        web.setLevel(logging.INFO)
        web.setFormatter(formatter)
        logger_web = logging.getLogger()
        logger_web.addHandler(web)

