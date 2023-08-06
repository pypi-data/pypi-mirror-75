"""
    Init file for Pyppet

    TODO: move imports to this location,
    TODO: to allow use as a stand alone module
"""

import logging
import os
from datetime import datetime

from . import sites, utlis

logger = logging.getLogger('root')

os.environ['PREVIOUS_SENSOR'] = ''

today = datetime.utcnow()
nowdate = today.strftime("%Y-%m-%d %H:%M:%S")


async def Launch():
    """
    Create Browser Object
    """
    utlis.disable_timeout_pyppeteer()
    return sites.make_browser
