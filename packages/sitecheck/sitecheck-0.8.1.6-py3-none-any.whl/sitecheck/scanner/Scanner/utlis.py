"""
    Geo-Instruments
    Sitecheck scanner
    Utilities Package for scanner

"""
import errno
import logging
import os
from pathlib import Path

from texttable import Texttable

from . import logger
from . import options
from .config import tuple_from_section_config
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
    # (Verbose) message
    if options.Debug:
        _format: str = '%(asctime)s - %(module)s - %(message)s'
    else:
        _format: str = '%(asctime)s - %(message)s'

    log = logging.getLogger(name)

    if options.Log:
        _log = Path(options.Output).joinpath(
            f'data//{filedate}//scan_report.log')
        ensure_exists(_log)

        with open(_log, 'a') as file:
            file.write(
                '\nRun Log for {filedate}\n=============================\n')
        logging.basicConfig(filename=_log, level=None, format=_format)
    else:
        logging.basicConfig(level=None, format=_format)

    if options.Debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    return log


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


def ensure_exists(path):
    """
    Accepts path to file, than creates the directory path if it does not exist
    :param path:
    :return:
    """
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return path


def projects_table(projects):
    """

    :param projects:
    """
    table = Texttable()
    table.set_cols_align(["l", "l", "l", "r"])
    table.set_cols_valign(["t", "t", "t", "t"])
    table.header(["Project Name", "Views to scan", "Platform", "Skipping"])
    for project in projects.sections():
        x = tuple_from_section_config(project)
        table.add_row([x.name, x.planarray, x.site, x.skip])
    return table.draw()
