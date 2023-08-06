"""
    Geo-Instruments
    Sitecheck scanner
    Data handler Package for scanner

"""
import os
import json

from . import logger
from sitecheck.scanner.Scanner import options

temp = os.environ.get('TEMP')


def check_mode(sensor: object) -> object:
    """
    Pauses run to give observer the chance to look at the information before proceeding.

    :return: Wait for input
    :rtype: object
    """
    if options.Repl:
        logger.log(sensor + ' is missing data')
        return input(
            "Pausing run for eval.\nPress Enter to continue...")


async def watchdog_handler(diff, project_name, sensor, date):
    """
    Handles sorting sensor watchdog status.

    Timeesamps from last update are sorted into three categories:
    Up-to-date, Behind, Old

    :param diff: Time since last reading
    :type diff: int

    :param project_name: Name of Project
    :type project_name: str

    :param sensor: Sensor ID
    :type sensor: str

    :param date: Formatted Date string
    :type date: str
    """
    # Sensor is Up-to-date.
    if diff <= options.Watchdog:
        data_list = [sensor, 'good', 'Up-to-date', date]
        logger.debug(data_list)
        if options.PrintNew:
            store(project_name, data_list)
    # Sensor is Behind.
    elif options.Watchdog <= diff <= options.Oldperiod:
        data_list = [
            sensor,
            'warning',
            'Older than %s hours' % options.args.time,
            date
            ]
        store(project_name, data_list)
        logger.info(data_list)
        check_mode(sensor)
    # Sensor is Old. Assumes after a week that this is a known issue.
    # Commonly these are blocked AMTS points
    else:
        data_list = [sensor, 'attention', 'Older than a week', date]
        logger.info(data_list)

        if options.PrintOld:
            store(project_name, data_list)
            check_mode(sensor)


def store(project, data_list):
    """
    Sensor Data storage function

    :param project:	Project name
    :type project: str

    :param data_list: Sensor data in list format
                Examples: ['IP2', 'good', 'Okay', '2020-01-16 08:00:00']
    :type data_list: list

    :rtype: None
    """
    file_path = f'{temp}//{project}_temp.txt'
    with open(file_path, 'a') as file:
        if not file.tell():
            file.write('[')
        else:
            file.write(',')
        file.write(json.dumps(data_list))
