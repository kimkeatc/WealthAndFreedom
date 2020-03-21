import logging
import sys


class Logger:

    def __init__(self, name=None):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        self.logger = logger

    def addStreamHandler(self, level=logging.INFO, formatter=None):
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        if not formatter:
            formatter = Logger.default_Formatter()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def addFileHandler(self, path, mode='a', level=logging.INFO, formatter=None):
        fh = logging.FileHandler(filename=path, mode=mode, encoding="utf-8")
        fh.setLevel(level)
        if not formatter:
            formatter = Logger.default_Formatter()
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    # Some default formatter options
    @staticmethod
    def default_DateFormat():
        return '%y/%m/%d %H:%M:%S'

    @staticmethod
    def default_MsgFormat():
        return '[%(asctime)s] [%(levelname)8s]: %(message)s'

    @staticmethod
    def default_Formatter():
        _msgFmt = Logger.default_MsgFormat()
        _dateFmt = Logger.default_DateFormat()
        fmt = logging.Formatter(_msgFmt, datefmt=_dateFmt)
        return fmt


if __name__ == '__main__':
    pass
