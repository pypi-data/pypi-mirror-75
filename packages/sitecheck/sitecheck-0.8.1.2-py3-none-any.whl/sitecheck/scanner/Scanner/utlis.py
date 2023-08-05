"""
    Geo-Instruments
    Sitecheck scanner
    Utilities Package for scanner

"""
import logging

from . import options


def make_logger(name) -> object:
    if options.Info:
        log_format: str = '%(asctime)s - %(message)s'
    elif options.Debug:
        log_format: str = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
    else:
        log_format: str = '%(message)s'
    logging.basicConfig(level=None, format=log_format)
    logger = logging.getLogger(name)
    if options.Info:
        logger.setLevel(logging.INFO)
    elif options.Debug:
        logger.setLevel(logging.DEBUG)
    return logger

