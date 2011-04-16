#!/usr/bin/python
# -*- coding: utf -*-

import datetime
import time

def timestamp(year=None, month=None, day=None):
    if year != None and month != None and day != None:
        return int(time.mktime((datetime.datetime(year, month, day)).timetuple()))
    else:
        return int(time.time())

def timestamp_ago(years=None, months=None, days=None):
    return int(time.mktime((datetime.datetime.now() + datetime.timedelta(years=years, months=months, days=days)).timetuple()))

def timestamp_format(timestamp):
    return (datetime.fromtimestamp(timestamp)).strftime('%d %b %Y')