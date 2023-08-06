"""
    Geo-Instruments
    Sitecheck scanner
    Project handler Package for scanner
"""
from sitecheck.scanner import logger
from sitecheck.scanner.Scanner.card_generator import adaptivecards
from sitecheck.scanner.Scanner.pyppet import sites
from sitecheck.scanner.Scanner.pyppet.amp import Amp_Webpage as amp
from sitecheck.scanner.Scanner.pyppet.quickview import Qv_Webpage as qv

from . import config
from . import options
from . import text
from . import utlis
from .text import filedate
from .utlis import ensure_exists


async def run_controller(project):
    """

        If --project is default, the "skip" value will be checked,
        Will than Scan the project or pass

        If --project is other than default. The first check will filter
        out the other projects silently, only running the given value.
        Cancels run if project.skip is true


    :returns: none

    """
    job = Project_runner(project)
    # Check for Default value 'All'
    if options.Project != 'All':
        # If not 'All' filter out everything except --project
        if options.Project == 'force':
            async with job:
                await job.project_site_handler()
        elif job.title == options.Project:
            async with job:
                await job.project_site_handler()
        else:
            return 0
    else:
        if job.project.skip == 'true':
            return f'Skipping project: {job.title}'
        else:
            async with job:
                await job.project_site_handler()


class Project_runner:
    """Project Run Object

    """

    def __init__(self, project_title):
        self.title = project_title
        self.project = config.tuple_from_section_config(project_title)
        name = self.project.name
        self.url = f'https://{self.project.name}.geo-instruments.com'
        self.temp: str = ensure_exists(
            f'{options.Output}//ARCHIVE//{filedate}//{name}.txt'
            )
        self.json: str = f'{options.Output}//{name}_card.json'

    async def __aenter__(self):
        await sites.make_browser(self)
        pages = await self.browser.pages()
        self.page = pages[0]
        await self.page.setViewport({"width": 1980, "height": 944})
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        config.edit_config_option(self.title, 'skip', 'true')
        try:
            if options.Repl:
                await self.browser.disconnect()
            else:
                await self.browser.close()
        except IOError:
            pass

    async def project_skip_handler(self):
        """
        Cancels run if project.skip is true

        If --project is other than default. The first check will filter
        out the other projects silently, only running the given value.

        If --project is default, the "skip" value will be checked, passing
        if true, or scanning the project is false.

        :return: Exit code
        :rtype: int
        """
        logger.debug(f'options.project: {options.Project}\n title: '
                     f'{self.title}\n'
                     f'skip: {self.project.skip}')
        if options.Project != 'All':
            if self.title == options.Project:
                return await self.project_site_handler()
            else:
                return 0
        else:
            if self.project.skip == 'true':
                return 1
            else:
                assert_file = await self.project_site_handler()
                # After a successful run, Set project skip = true
                config.edit_config_option(self.title, 'skip', 'true')
                return 0

    async def project_site_handler(self):
        """
        Checks if a project is housed on Amp, Qv, and/or Truelook.
        """
        logger.info(f'{self.project.name} {text.fileheader}')
        logger.debug(f'Project:    {self.project.name}')
        logger.debug(f'Has Site:   {self.project.site}')
        logger.debug(f'Plan array: {self.project.planarray}\n')
        utlis.remove_file(self.temp, self.json)

        if self.project.site == 'amp':
            await self.amp_runner()
        elif self.project.site == 'qv':
            await self.qv_runner()
        elif self.project.site == 'truelook':
            return str('In Development')

        staged_file = adaptivecards.Generator(self.project)
        path_to_temp = staged_file.compile_data()

        return path_to_temp

    async def amp_runner(self):
        """
        Main Operator of the Amp scanner.

        Creates the new page and gives it a viewport.
        Than handles gathering and output of data for Amp scanner.
        """
        logger.info('Launching Amp..')
        await sites.login(self)
        await amp.goto_plan_view(self)

    async def qv_runner(self):
        """
        Main Operator of the QV scanner.

        Handles gathering and output of data for QV scanner.
        """
        logger.info('Launching QV..')
        self.url = 'https://quickview.geo-instruments.com/login.php'
        await sites.login(self)
        await qv.goto_project(self)
        await qv.goto_plan_view(self)
