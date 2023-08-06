"""
    Geo-Instruments
    Sitecheck scanner
    Command Line argument Parser for scanner
    Provides handling of arguments passed from command line
    These can be made permenant by adding them to your shortcut path
"""

import argparse
import os
from pathlib import Path

from sitecheck.scanner.Scanner import config
from .utlis import ensure_exists

projects = config.read_config_file()

ROOT_card: str = ensure_exists(str(
    Path(os.environ['OneDriveCommercial'] + "//scanner//")
    ))

chrome_args = ['--window-size=1980,944']  # '--kiosk''


class Formatter(argparse.RawDescriptionHelpFormatter):
    """argparse.RawDescriptionHelpFormatter
        Provides formatting settings for argument "Help" messages.
        Can add argparse.ArgumentDefaultsHelpFormatter for defaults.
    """
    pass


class arg_text:
    """
        Text for --help

        Members include:
            main, old,
            new, watchdog,
            headless, chechmode
    """
    main: str = """
    Automated Sitecheck Toolkit for Geo-Instruments Field Technicians
    \nSensors are sorted into three categories:
    \nUp-to-date:    Most recent data is within 24 hours
    \nOverdue:       Instrument is behind
    \nOld:           Reading has been missing for over a week
    \nAn Adaptive card containing missing sensor information is sent the user
    via Microsfot Team's Flowbot
    \nUser can push Cards into their Regional Sitecheck channel of choice.
    """
    info: str = 'Set logging level to Info'
    debug: str = 'Set logging level to Debug'
    log: str = f'Saves stout to log file located at \"{ROOT_card}' \
               '/data/filedata/run_report.log\"'
    edit: str = 'Opens projects file in editor'
    project_builtins: str = 'force, qv, amp'
    project: str = f'Define a single project to run. Availble Options include {project_builtins} ' \
                   f'Options: {str(projects.sections())}. '
    time: str = 'Set number of hours to mark as \'Up-to-date\' \n ' \
                '\'Old\' is a 7 times multiple of this value. ' \
                'Example: --time 24'
    test: str = 'Run program up until time of browser creation ' \
                'for testing purposes.'
    repl: str = 'read–eval–print loop (REPL) Interactive command mode'
    old: str = 'Include in report sensors missing for Longer than a week. ' \
               'This is off by default, Assumes sensors missing for 7 days ' \
               'are discussed.'
    new: str = 'Include in report sensors that pass checks. This is off by ' \
               'default to prevent unnecessary spam'
    headless: str = 'Enables Pyppeteer\'s Headless mode. The browser ' \
                    'will run invisibly, Known Issues with Qv navigation ' \
                    'are being addressed'
    putput: str = 'Set card output directory'
    value: str = 'Include current Sensor data in output'
    weather: str = 'Include local weather data in status report'
    screenshot: str = 'Save a screenshot when a sensor is missing'


parser = argparse.ArgumentParser(
    description=arg_text.main,
    prog='Sitecheck Scanner',
    formatter_class=Formatter
    )

parser.add_argument('-r', '--repl', action='store_true', default=False,
                    help=argparse.SUPPRESS)  # help=arg_text.repl)
parser.add_argument('-H', '--headless', action='store_true', default=False,
                    help=argparse.SUPPRESS)  # help=arg_text.hadless)

parser.add_argument('-i', '--info', action='store_true', default=True,
                    help=arg_text.info)

parser.add_argument('-d', '--debug', action='store_true', default=False,
                    help=arg_text.debug)

parser.add_argument('-l', '--log', action='store_true', default=False,
                    help=arg_text.log)

parser.add_argument('-e', '--edit', action='store_true', default=False,
                    help=arg_text.edit)

parser.add_argument('-p', '--project', default='All',
                    choices=projects.sections(), metavar='',
                    help=arg_text.project)

parser.add_argument('-t', '--time', default='24', metavar='', type=int,
                    help=arg_text.time)

parser.add_argument('--test', action='store_true', default=False,
                    help=arg_text.test)

parser.add_argument('-O', '--old', action='store_true', default=False,
                    help=arg_text.old)

parser.add_argument('-N', '--new', action='store_true', default=False,
                    help=arg_text.new)

parser.add_argument('-o', '--output', action='store', type=str, metavar='',
                    default=ROOT_card,
                    help=argparse.SUPPRESS)  # help=arg_text.output)

parser.add_argument('-v', '--value', action='store_true', default=False,
                    help=argparse.SUPPRESS)  # help=arg_test.value)

parser.add_argument('-w', '--weather', action='store_true',
                    help=argparse.SUPPRESS)  # help=arg_test.weather)

parser.add_argument('-s', '--screenshot', action='store_true', default=False,
                    help=argparse.SUPPRESS)  # help=arg_test.screenshot)

args = parser.parse_args()

Info: bool = args.info
Debug: bool = args.debug
Log: bool = args.log
Edit: bool = args.edit
Project: str = args.project
Watchdog: int = int(args.time * 3600)
Test: bool = args.test
Repl: bool = args.repl
PrintOld: bool = args.old
PrintNew: bool = args.new
Headless: bool = args.headless
Output: str = args.output
Getvalue: bool = args.value
Weather: bool = args.weather
Screenshot: bool = args.screenshot

Oldperiod: int = 604800

