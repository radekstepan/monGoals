#!/usr/bin/python
# -*- coding: utf -*-

# framework
from flask import Module

from models.cdn import CDN

cdn = Module(__name__)

@cdn.route('/cdn/image/<id>')
def image(id):
    '''fetch a base64 encoded image from the db'''
    c = CDN()
    file = c.find_one(id)

    return file['image']