"""
    Geo-Instruments
    Sitecheck scanner
"""
# __author__ = "Dan Edens"
# __url__= "https://github.com/DanEdens/Sitecheck_Scrapper"
# __status__  = "production"

import logging, os

logger = logging.getLogger('root')
ROOT_DIR = os.environ['ROOT_DIR']
projectstore = ROOT_DIR + '\\projects.ini'
