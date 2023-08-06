"""
    Quickview navigation functions for Scanner.pyppet module
"""
import os

import dateutil.parser
from dateutil.parser import parse
from pyppeteer.errors import *

from sitecheck.scanner import logger
from sitecheck.scanner.Scanner import data
from . import sites
from . import text
from . import utlis
from .text import Qv_text


class Qv_Webpage:
    """
    Operator pool for QV
    """

    async def goto_project(self):
        """
        Navigates to project as defined by project.proj and iterates
        through project views

        :rtype: None
        """
        await utlis.wait_click(self.page,
                               '.sidebar-wrapper > .nav > '
                               '#menuProjects > a > p'
                               )
        await utlis.wait_hover(self.page, Qv_text.scrollbar)
        await self.page.waitFor(500)
        await utlis.wait_type(self.page, '.wrapper #projectSearchInput',
                              self.project.name)
        await self.page.waitFor(500)
        await utlis.wait_hover(self.page, Qv_text.scrollbar)
        await self.page.waitFor(500)
        await utlis.wait_click(self.page,
                               "#projectList > div > div.panelRowTxt2")

    async def goto_plan_view(self):
        """
        Navigates to each planview listed in project.planarray and iterates through
        hoving on each sensor, gathering data from the loaded Hoverbox

        :rtype: None
        """
        views = self.project.planarray.split(",")
        for view in views:
            logger.debug('Scanning Planview: ' + view)
            if view == '0':
                pass
            else:
                await utlis.wait_click(self.page, Qv_text.views)
                await self.page.waitFor(500)
                await utlis.wait_hover(self.page, Qv_text.scrollbar2)
                await self.page.waitFor(300)
                logger.info('Navigating to view #' + view)
                await utlis.wait_click(self.page, Qv_text.thumb + view)
            await utlis.wait_count(self, 5)
            await sites.scan_plan_view(self, Qv_Webpage)

    async def get_last_update(self):
        """
        Collects Sensor data for the provided
        sensor: int = os.environ['TARGET_CHILD']

        Passes over non-existent sensors during view scan.
        raise PageError('No node found for selector: ' + selector)
        pyppeteer.errors.PageError:
        No node found for selector: #objects > img:nth-child(0)

        :raises: pyppeteer.errors.PageError

        :rtype: None
        """
        sensor = '#objects > img:nth-child(' + os.environ['TARGET_CHILD'] + ')'
        try:
            await self.page.hover(sensor)
            _link = await self.page.J(Qv_text.hoverbox)
            _txt = await self.page.evaluate('(link) => link.innerHTML', _link)
            _split_date = _txt.split('<br>')
            sensor = _split_date[0]
            if sensor != os.environ['PREVIOUS_SENSOR']:
                os.environ['PREVIOUS_SENSOR'] = sensor
                sensor_data = '\nSensor name: ' + sensor
                date = _split_date[3].split("data: ").pop()
                sensor_data += '\nLatest data on QV: '
                diff_in_days = parse(text.nowdate) - parse(date)
                diff = (diff_in_days.total_seconds())
                sensor_data += date
                await data.watchdog_handler(
                    diff,
                    self.project.name,
                    sensor,
                    date
                    )
        except (ElementHandleError, PageError, IndexError):
            pass
        except dateutil.parser.ParserError:
            logger.warn("Sensor has no data to compare")
