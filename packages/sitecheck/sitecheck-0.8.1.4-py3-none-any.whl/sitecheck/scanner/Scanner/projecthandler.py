"""
    Geo-Instruments
    Sitecheck scanner
    Project handler Package for scanner
"""

from sitecheck.scanner import logger
from sitecheck.scanner.Scanner import config
from sitecheck.scanner.Scanner import options
from sitecheck.scanner.Scanner import text
from sitecheck.scanner.Scanner import utlis
from sitecheck.scanner.Scanner.card_generator import adaptivecards
from sitecheck.scanner.Scanner.pyppet import amp
from sitecheck.scanner.Scanner.pyppet import quickview
from sitecheck.scanner.Scanner.pyppet import sites
from sitecheck.scanner.Scanner.pyppet.sites import make_browser


async def run_controller(project):
    """
    :param project: Object containing project.sections() data:
        hassite, name, playarray, proj, skip, channel
    :param browser: Object created by await pyppet.Launch()

    :returns: none

    """
    job = Project_runner(project)
    result: int = await job.project_skip_handler()

    if result == 0:
        logger.debug(result)
    elif result == 1:
        logger.debug(f'Skipping project: {project}')


class Project_runner:
    """Project Run Object"""

    def __init__(self, project_title):
        self.title = project_title
        self.project = config.tuple_from_section_config(project_title)
        name = self.project.name
        self.url = f'https://{self.project.name}.geo-instruments.com'
        self.temp: str = f'{options.Storage}//{name}_temp.txt'
        self.json: str = f'{options.Output}//{name}_card.json'

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
        if options.Project != 'All' and self.title == options.Project:
            if self.title == options.Project:
                return await self.project_site_handler()
            else:
                return 0
        else:
            if self.project.skip == 'true':
                return 1
            else:
                await self.project_site_handler()
                # After a successful run, Set project skip = true
                config.edit_config_option(self.title, 'skip', 'true')
                return 0

    async def project_site_handler(self):
        """
        Checks if a project is housed on Amp, Qv, and/or Truelook.
        """
        logger.info(f'{self.project.name} {text.fileheader}')
        logger.debug(f'Project:    {self.project.name}')
        logger.debug(f'Skip:       {self.project.skip}')
        logger.debug(f'Has Site:   {self.project.site}')
        logger.debug(f'Plan array: {self.project.planarray}\n')
        utlis.remove_file(self.temp, self.json)

        global browser
        browser = await make_browser()
        pages = await browser.pages()
        self.page = pages[0]
        await self.page.setViewport({"width": 1980, "height": 944})

        if self.project.site == 'amp':
            await self.amp_runner()
        elif self.project.site == 'qv':
            await self.qv_runner()
        elif self.project.site == 'truelook':
            return str('In Development')

        try:
            if options.Checkmode:
                await browser.disconnect()
            else:
                await browser.close()
        except IOError:
            pass

    async def amp_runner(self):
        """
        Main Operator of the Amp scanner.

        Creates the new page and gives it a viewport.
        Than handles gathering and output of data for Amp scanner.
        """
        logger.info('Launching Amp..')

        await sites.login(self)
        await amp.Amp_Webpage.goto_plan_view(self)
        logger.info(self.project.name)

        staged_file = adaptivecards.Generator(self.project)
        path_to_temp = staged_file.compile_data()

    async def qv_runner(self):
        """
        Main Operator of the QV scanner.

        Handles gathering and output of data for QV scanner.
        """
        logger.info('Launching QV..')
        self.url = 'https://quickview.geo-instruments.com/login.php'

        await sites.login(self)
        await quickview.Qv_Webpage.goto_project(self)
        await self.page.waitFor(500)

        await quickview.Qv_Webpage.goto_plan_view(self)
        staged_file = adaptivecards.Generator(self.project)
        path_to_temp = staged_file.compile_data()
        if options.Checkmode:
            await browser.disconnect()
        else:
            try:
                await browser.close()
            except IOError:
                pass
        return path_to_temp
