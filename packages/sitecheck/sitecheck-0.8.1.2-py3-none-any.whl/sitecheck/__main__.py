"""
    Geo-Instruments
    Sitecheck scanner

    Load project configs from 'project.ini', and loop through the views listed.
    Each project run retrieves Sensor data from Amp or QV, and produces an Adaptive card.
    Default output is in "~\\OneDrive - Keller\\scanner\\" for the Teams Flowbow to ingest

"""
# __author__ = "Dan Edens"
# __version__= "0.8.1.2"
# __url__= "https://geodev.geo-instruments.com/DanEdens/Sitecheck_Scanner"

import asyncio

from sitecheck.scanner import Sitecheck


async def main():
    """Main Entry point for scanner"""
    await Sitecheck()


if __name__ == "__main__":
    """Prevents main from running when imported"""
    asyncio.run(main())
