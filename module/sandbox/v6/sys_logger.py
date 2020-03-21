import logging
import sys

def _formatter(msg_fmt, time_fmt):
    mfmt = "[%(asctime)s] %(levelname)10s : %(message)s"
    tfmt = "%Y-%m-%d %H:%M:%S"
    if msg_fmt:
        mfmt = msg_fmt
    if time_fmt:
        tfmt = time_fmt
    return logging.Formatter(mfmt, tfmt)

def _setup_clogger(msg_fmt, time_fmt):
    log = logging.StreamHandler(sys.stdout)
    log.setLevel(logging.DEBUG)
    log.setFormatter(_formatter(msg_fmt, time_fmt))
    return log

def _setup_flogger(path, msg_fmt, time_fmt):
    log = logging.FileHandler(path, "w")
    log.setLevel(logging.DEBUG)
    log.setFormatter(_formatter(msg_fmt, time_fmt))
    return log

def setup(flog=None, clog=True, msg_fmt=None, time_fmt=None):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if flog:
        logger.addHandler(_setup_flogger(flog, msg_fmt, time_fmt))
    if clog:
        logger.addHandler(_setup_clogger(msg_fmt, time_fmt))
    
    return logger
