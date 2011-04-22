#!/usr/bin/python
# -*- coding: utf -*-

import datetime
import time
import shlex

def timestamp_new(year=None, month=None, day=None):
    if year != None and month != None and day != None:
        return int(time.mktime((datetime.datetime(int(year), int(month), int(day))).timetuple()))
    else:
        return int(time.time())

def timestamp_ago(years=None, months=None, days=None):
    return int(time.mktime((datetime.datetime.now() + datetime.timedelta(years=years, months=months, days=days)).timetuple()))

def timestamp_format(timestamp):
    return (datetime.date.fromtimestamp(timestamp)).strftime('%a, %d %b %Y').replace(' 0', ' ')

def date_list(timestamp):
    return [int(x) for x in shlex.split((datetime.date.fromtimestamp(timestamp)).strftime('%d %m %Y').replace(' 0', ' '))]