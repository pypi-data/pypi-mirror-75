"""
    Geo-Instruments
    Sitecheck scanner
    Utilities Package for scanner

"""
import logging
import os
from pathlib import Path

from . import logger
from . import options
from .text import filedate


def make_logger(name) -> object:
    """
    Create the project wide logger.
    Sets Output level from Argument flags and if output should be directed
    to a log file.
    Default location is Onedrive/scanner
    :param name:
    :return: Logger
    :rtype: Object
    """
    if options.Info:
        _format: str = '%(asctime)s - %(message)s'
    elif options.Debug:
        _format: str = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
    else:
        _format: str = '%(message)s'
    if options.Log:
        _log = Path(
            os.environ['OneDriveCommercial']
            ).joinpath(
            'scanner//logs//%srun_report.log' % filedate
            )
        with open(_log, 'a') as file:
            file.write('Run Log for %s' % filedate)
        logging.basicConfig(filename=_log, level=None, format=_format)
    else:
        logging.basicConfig(level=None, format=_format)
    logging.basicConfig(level=None, format=_format)
    logger = logging.getLogger(name)
    if options.Info:
        logger.setLevel(logging.INFO)
    elif options.Debug:
        logger.setLevel(logging.DEBUG)
    return logger


def remove_file(*args):
    """
    Removes Old copy of **file** is file exists
    :param file: File to be replaced
    :return: none

    """
    for file in args:
        try:
            os.remove(file)
            logger.debug('Removing previous copy of %s.. ' % file)
        except OSError:
            pass
