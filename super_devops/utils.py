import os
import logging


class Utils(object):

    @staticmethod
    def expandpath(path):
        if path:
            real_path = path
        if '~' in path:
            real_path = os.path.expanduser(path)
        if '$' in path:
            real_path = os.path.expandvars(path)
        if '..' in path:
            real_path = os.path.abspath(path)
        return real_path

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

