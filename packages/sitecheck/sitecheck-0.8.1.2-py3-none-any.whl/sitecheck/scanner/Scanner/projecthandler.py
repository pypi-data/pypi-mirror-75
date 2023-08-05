"""
    Geo-Instruments
    Sitecheck scanner
    Project handler Package for scanner
"""


import os


from sitecheck.scanner import logger
from sitecheck.scanner.Scanner import options, config, text
from sitecheck.scanner.Scanner.card_generator import adaptivecards
from sitecheck.scanner.Scanner.pyppet import amp, quickview, sites
from sitecheck.scanner.Scanner.pyppet.sites import make_browser

async def run_controller(project):
    """
    :param project: Object containing project.sections() data:
        hassite, name, playarray, proj, skip, channel
    :param browser: Object created by await pyppet.Launch()

    :returns: none

    """
    run_result = Project_runner(project)
    result = await run_result.skip_site()
    logger.debug(result)


class Project_runner:
    """

    """

    def __init__(self, project):
        self.project = config.tuple_from_section_config(project)

    async def skip_site(self):
        """
        Cancels run if project.skip is true
        """
        if options.project != 'All':
            if self.project.name in options.project:
                return await self.filter_site()
        else:
            if self.project.skip == 'true':
                return str('Skipping project: ' + self.project.name)
            else:
                return await self.filter_site()

    async def filter_site(self):
        """
        Checks if a project is housed on Amp, Qv, and/or Truelook.
        """
        logger.info(self.project.name + text.fileheader)
        logger.debug('Project:    ' + self.project.name)
        logger.debug('Skip:       ' + self.project.skip)
        logger.debug('Has Site:   ' + self.project.site)
        logger.debug('Plan array: ' + self.project.planarray + '\n')
        # TODO: create clean function in utlis
        if os.path.exists(os.environ.get('TEMP') + self.project.name + '_temp.txt'):
            logger.debug('Deleting old temp file: ' + self.project.name)
            os.remove(os.environ.get('TEMP') + self.project.name + '_temp.txt')
        if os.path.exists(options.output + self.project.name + '_card.json'):
            logger.debug('Deleting old json file: ' + self.project.name)
            os.remove(options.output + self.project.name + '_card.json')
        if self.project.site == 'amp':
            await self.amp_runner()
        elif self.project.site == 'qv':
            await self.qv_runner()
        elif self.project.site == 'truelook':
            logger.warning('In Development')

    async def amp_runner(self):
        """
        Main Operator of the Amp scanner.

        Creates the new page and gives it a viewport.
        Than handles gathering and output of data for Amp scanner.
        """
        logger.info('Launching Amp..')
        browser = await make_browser()
        pages = await browser.pages()
        self.page = pages[0]
        self.url = 'https://' + self.project.name + '.geo-instruments.com/index.php'
        await self.page.setViewport({"width": 1980, "height": 944})
        await sites.login(self)
        await amp.Amp_Webpage.goto_plan_view(self)
        logger.info(self.project.name)
        staged_file = adaptivecards.Generator(self.project)
        path_to_temp = staged_file.compile_data()
        if options.Checkmode:
            await browser.disconnect()
        else:
            await browser.close()
        return path_to_temp

    async def qv_runner(self):
        """
        Main Operator of the QV scanner.

        Handles gathering and output of data for QV scanner.
        """
        logger.info('Launching QV..')
        browser = await make_browser()
        pages = await browser.pages()
        self.page = pages[0]
        self.url = 'https://quickview.geo-instruments.com/login.php'
        await self.page.setViewport({"width": 1980, "height": 944})
        await sites.login(self)
        await quickview.Qv_Webpage.goto_project(self)
        await self.page.waitFor(500)

        await quickview.Qv_Webpage.goto_plan_view(self)
        staged_file = adaptivecards.Generator(self.project)
        path_to_temp = staged_file.compile_data()
        if options.Checkmode:
            await browser.disconnect()
        else:
            await browser.close()
        return path_to_temp
