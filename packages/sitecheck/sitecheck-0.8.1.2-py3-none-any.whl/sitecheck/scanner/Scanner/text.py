"""
    Geo-Instruments
    Sitecheck scanner
    Text Package for scanner

"""
import datetime

today = datetime.datetime.utcnow()
nowdate = today.strftime("%Y-%m-%d %H:%M:%S")
fileheader = 'scan for ' + nowdate
no_channel = 'Channel name does not match configured projects'
uptoDate = 'Most recent data is within 24 hours\n'
behindDate = 'Instrument is behind\n'
oldDate = 'Reading has been missing for over a week\n'
loginmessage = 'Login Successful.'
