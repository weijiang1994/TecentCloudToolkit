"""
coding:utf-8
file: log.py
@time: 2024/7/3 23:21
@desc:
"""
import logging


class LogUtil:

    def __init__(
            self,
            name,
            file_path=None,
            format_str='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG,
            encoding='utf-8'
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter(format_str)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        if file_path:
            fh = logging.FileHandler(file_path, encoding=encoding)
            fh.setLevel(level)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

        self.log_level_func = {
            'debug': self.logger.debug,
            'info': self.logger.info,
            'warning': self.logger.warning,
            'error': self.logger.error,
            'critical': self.logger.critical,
            'exception': self.logger.exception
        }

    def write_log(self, msg, level='info'):
        self.log_level_func[level](msg)

    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    @staticmethod
    def get_file_logger(name, file_path):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh = logging.FileHandler(file_path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    @staticmethod
    def get_logger_with_file(name, file_path):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        fh = logging.FileHandler(file_path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(fh)
        return logger
