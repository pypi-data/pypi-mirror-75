"""
    Geo-Instruments
    Sitecheck scanner

    CLI entry point and function pool
"""
# __author__ = "Dan Edens"
# __url__= "https://github.com/DanEdens/Sitecheck_Scrapper"
# __status__  = "production"

import os

from sitecheck.scanner.Scanner import config
from sitecheck.scanner.Scanner import options
from sitecheck.scanner.Scanner import utlis

logger = utlis.make_logger('root')
ROOT_DIR = os.environ['ROOT_DIR']

projects = config.read_config_file()


async def Sitecheck():
    """
    Invoke to Scan all projects marked with "skip = false" in projects.ini
    """
    # logger.info("Available Projects: (Short names)")
    # logger.info(texttable(projects.sections(), headers=['\nProject:'],
    #                      tablefmt="Pretty"))

    from sitecheck.scanner.Scanner import projecthandler

    [await (projecthandler.run_controller(project)) for project in
     projects.sections()]
    logger.info('\nScan completed.')


def edit():
    """
    Edits project config file
    """

    if options.Edit:
        config.edit_project()
