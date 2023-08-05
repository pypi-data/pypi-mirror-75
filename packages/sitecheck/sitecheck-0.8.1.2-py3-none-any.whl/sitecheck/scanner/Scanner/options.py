"""
    Geo-Instruments
    Sitecheck scanner
    Command Line argument Parser for scanner

"""

import os
import argparse

from . import config


class Formatter(argparse.RawDescriptionHelpFormatter):
    """

    argparse.RawDescriptionHelpFormatter
        Provides formatting options for cli arguments and output.
        Can add argparse.ArgumentDefaultsHelpFormatter for defaults. May turn this into flag
    """
    pass


class arg_text:
    """
        Text for --help
    """
    main = """
    Automated Sitecheck Toolkit for Geo-Instruments Field Technicians
    \nSensors are sorted into three categories:
    \nUp-to-date:    Most recent data is within 24 hours
    \nOverdue:       Instrument is behind
    \nOld:           Reading has been missing for over a week
    \nAn Adaptive card containing missing sensor information is sent the user via Microsfot Team's Flowbot 
    \nUser can push Cards into their Regional Sitecheck channel of choice.
    """
    old = 'Include in report sensors missing for Longer than a week. This is off by default, Assumes sensors missing for 7 days are discussed.'
    new = 'Include in report sensors that pass checks. This is off by default to prevent unnecessary spam'
    watchdog = 'Set number of hours to mark as \'Up-to-date\' \n \'Old\' is a 7 times multiple of this value. Example: --time 24'
    headless = 'Enables Pyppeteer\'s Headless mode. The browser will run invisibly, Known Issues with Qv navigation are being addressed'
    checkmode = 'Enables a pause in the run whenever a sensor is detected to be missing data. Run will proceed when ' \
                'key is pressed on command line '


ROOT_card = (os.environ.get('USERPROFILE')+"\\OneDrive - Keller\\scanner\\")
chrome_args = ['--window-size=1980,944']  # '--kiosk''
projects = config.read_config_file()
parser: argparse.ArgumentParser = argparse.ArgumentParser(description=arg_text.main, prog='Sitecheck scanner', formatter_class=Formatter)
parser.add_argument('-i', '--info', action='store_true', default=False, help='Set logging level to Info')
parser.add_argument('-d', '--debug', action='store_true', default=False, help='Set logging level to Debug')
parser.add_argument('-e', '--edit', action='store_true', default=False, help='Opens projects file in editor')
parser.add_argument('-p', '--project', default='All', choices=projects.sections(), metavar='', help='Define a single project to run. Options: '+str(projects.sections()))
parser.add_argument('-hh', '--test', action='store_true', default=False, help='Run program up until time of browser creation for testing purposes.')
parser.add_argument('-c', '--check', action='store_true', default=False, help=argparse.SUPPRESS)  # help=arg_text.checkmode)
parser.add_argument('-O', '--old', action='store_true', default=False, help=arg_text.old)
parser.add_argument('-N', '--new', action='store_true', default=False, help=arg_text.new)
parser.add_argument('-H', '--headless', action='store_true', default=False, help=arg_text.headless)
parser.add_argument('-o', '--output', action='store', type=str, metavar='', default=ROOT_card, help=argparse.SUPPRESS)  # help='Set card output directory')
parser.add_argument('-t', '--time', default='24', metavar='', type=int, help=argparse.SUPPRESS)  # help=arg_text.watchdog)
parser.add_argument('-v', '--value', action='store_true', default=False, help=argparse.SUPPRESS)  # help='Include current Sensor data in output')
parser.add_argument('-w', '--weather', action='store_true', help=argparse.SUPPRESS)  # help='Include local weather data in status report')
parser.add_argument('-s', '--screenshot', action='store_true', default=False, help=argparse.SUPPRESS)  # help='Save a screenshot when a sensor is missing')
args = parser.parse_args()
watchdog = int(args.time * 3600)
project = args.project
PrintOld = args.old
PrintNew = args.new
Checkmode = args.check
edit = args.edit
output = args.output or ROOT_card
screenshot = args.screenshot
Debug = args.debug
Info = args.info
headless = args.headless
getvalue = args.value
Test = args.test
