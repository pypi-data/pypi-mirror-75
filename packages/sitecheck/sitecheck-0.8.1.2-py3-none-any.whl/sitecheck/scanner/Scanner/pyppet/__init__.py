"""
    Init file for Pyppet
"""
# __author__ = DanEdens
# __status__  = "production"

import logging
import os

import sitecheck.scanner.Scanner

from . import sites, utlis

logger = logging.getLogger('root')

os.environ['PREVIOUS_SENSOR'] = 'initstr'


async def Launch():
    """
    Create Browser Object
    """
    utlis.disable_timeout_pyppeteer()
    return sites.make_browser
