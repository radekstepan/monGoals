#!/usr/bin/python
# -*- coding: utf -*-

from pymongo import Connection

db = None

def init_connection(database):
    global db

    connection = Connection()
    db = connection[database]

def database_name():
    '''get database name'''
    return db.database.database.name

def table_drop(tablename):
    global db
    
    db.drop_collection(tablename)