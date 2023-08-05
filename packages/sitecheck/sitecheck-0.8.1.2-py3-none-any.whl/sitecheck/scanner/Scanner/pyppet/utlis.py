"""
    Utilities Package for Pyppet
"""
import os

from sitecheck.scanner import ROOT_DIR, logger


def get_date() -> str:

    import datetime
    today = datetime.datetime.utcnow()
    return str(today.strftime("%Y-%m-%d"))


def make_logger() -> object:
    import logging
    log_format: str = '%(asctime)-15s - %(message)s'
    logging.basicConfig(level=None, format=log_format)
    logger = logging.getLogger(__name__.split('.')[0])
    # if options.Debug:
    #     logger.setLevel(logging.DEBUG)
    # elif options.Verbose:
    logger.setLevel(logging.INFO)
    return logger


async def wait_type(page, selector, txt):
    """
    :param: page
    :param: selector
    :param: txt

    Wait for a selector to load than type supplied text.

    :returns: page
        This is in case the pages response to text changes the browser context.

    """
    await page.waitForSelector(selector)
    await page.type(selector, txt)
    return page


async def wait_click(page, selector):
    """
    :param: page
    :param: selector

    Wait for a selector to load, than click on it.

    :returns: page
        This is in case click navigation changes the browser context.
    """
    await page.waitForSelector(selector),
    await page.click(selector)
    return page


async def wait_hover(page, selector):
    """
    :param: page
    :param: selector

    Wait for a selector to load, than hover over it.

    :returns: page
        This is in case page response changes the browser context.
    """
    await page.waitForSelector(selector),
    await page.hover(selector)
    return page


async def screenshot(self, sensor, name_sel):
    logger.warn('Feature is disabled')
    return
    project_images = ROOT_DIR+'\\Screenshots\\'+self.project.name+'\\'
    if os.path.exists(project_images):
        pass
    else:
        os.makedirs(project_images)
    await wait_hover(self.page, name_sel)
    await self.page.waitFor(500)
    await self.page.screenshot({'path': project_images+sensor+'_'+get_date()+'.png'})


def disable_timeout_pyppeteer():
    """
        :Pyppeteer upstream depricates need for this:
        Disables built-in max browser interation Timeout

        :returns: original_method(*args, **kwargs)
    """
    import pyppeteer.connection
    original_method = pyppeteer.connection.websockets.client.connect

    def new_method(*args, **kwargs):
        kwargs['ping_interval'] = None
        kwargs['ping_timeout'] = None
        return original_method(*args, **kwargs)

    pyppeteer.connection.websockets.client.connect = new_method


async def wait_count(self, count):
    wait_time = count
    while wait_time > 0:
        logger.info("Waiting (%s) seconds for Page load.." % str(wait_time))
        wait_time -= 1
        await self.page.waitFor(1000)
    return None
