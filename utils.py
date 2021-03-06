#!/usr/bin/python
# -*- coding: utf -*-

# time & date
import datetime
import time

# string split
import shlex

# file upload
from pymongo.binary import Binary
from werkzeug import secure_filename
import os
import Image

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

def sort_list(list):
    return sorted(list, key=lambda k: k['date'])

def sort_list_by_points(list):
    return sorted(list, key=lambda k: k['points']['target'], reverse=True)

def file_to_mongo(file):
    # upload
    path = os.path.join('static/temp', secure_filename(file.filename))
    file.save(path)
    # resize
    size = 300, 222
    img = Image.open(path)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(path)
    # convert
    string = Binary(open(path, "rb").read().encode("base64"))
    # remove
    os.remove(path)
    # return
    return string

def slugify(value):
    import unicodedata, re

    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)