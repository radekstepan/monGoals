#!/usr/bin/python
# -*- coding: utf -*-

# db
from bson.objectid import ObjectId
from pymongo import ASCENDING
from db import db

class Goals:

    table = db.goals

    def find_one(self, id):
        return self.table.find_one({"_id": ObjectId(id)})

    def find_all(self):
        return self.table.find().sort("date.end", ASCENDING)

    def find(self, where):
        return self.table.find(where).sort("date.end", ASCENDING)

    def save(self, dict):
        return self.table.insert(dict)

    def update(self, id, what, dict):
        self.table.update({'_id': ObjectId(id)}, {"$set": {what: dict}})

    def remove(self, id):
        self.table.remove({'_id': ObjectId(id)})

    def increment(self, id, what, value):
        self.table.update({'_id': ObjectId(id)}, {"$inc": {what: value}})

    def to_list(self, object):
        list = []
        for entry in object:
            list.append(entry)
        return list