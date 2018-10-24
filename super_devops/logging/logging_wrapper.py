import logging


class BaseLogging(object):
    def __init__(self, name=None, format=None):
        if not format:
            self.format = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
        else:
            self.format = format
        self.logger = logging.getLogger(name)

    def init_logger(
            self, log_file=None, log_mode='a', log_level=logging.DEBUG
    ):
        try:
            logging.basicConfig(
                level=log_level,
                format=self.format,
                filename=log_file,
                filemode=log_mode
            )
            formatter = logging.Formatter(self.format)

            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            console.setFormatter(formatter)
            logger = logging.getLogger()
            logger.addHandler(console)
        except Exception as e:
            raise RuntimeError(
                "Init logger failed: {}".format(e.message)
            )
        else:
            return self.logger

    def init_debug_and_info_logger(
            self, debug_file=None, debug_mode='a',
            info_file=None, info_mode='a'
    ):
        try:
            logging.basicConfig(
                level=logging.DEBUG,
                format=self.format,
                filename=debug_file,
                filemode=debug_mode
            )
            formatter = logging.Formatter(self.format)

            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            console.setFormatter(formatter)
            logger = logging.getLogger()
            logger.addHandler(console)

            web = logging.FileHandler(info_file, info_mode)
            web.setLevel(logging.INFO)
            web.setFormatter(formatter)
            logger_web = logging.getLogger()
            logger_web.addHandler(web)
        except Exception as e:
            raise RuntimeError(
                "Init debug&info logger failed: {}".format(e.message)
            )
        else:
            return self.logger

    def init_debug_and_warn_logger(
            self, debug_file=None, debug_mode='a',
            warn_file=None, warn_mode='a'
    ):
        try:
            logging.basicConfig(
                level=logging.DEBUG,
                format=self.format,
                filename=debug_file,
                filemode=debug_mode
            )
            formatter = logging.Formatter(self.format)

            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            console.setFormatter(formatter)
            logger = logging.getLogger()
            logger.addHandler(console)

            web = logging.FileHandler(warn_file, warn_mode)
            web.setLevel(logging.WARN)
            web.setFormatter(formatter)
            logger_web = logging.getLogger()
            logger_web.addHandler(web)
        except Exception as e:
            raise RuntimeError(
                "Init debug&warn logger failed: {}".format(e.message)
            )
        else:
            return self.logger

