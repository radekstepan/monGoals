#!/usr/bin/python
# -*- coding: utf -*-

# db
from bson.objectid import ObjectId
from db import db

class CDN:

    table = db.cdn

    def find_one(self, id):
        return self.table.find_one({"_id": ObjectId(id)})

    def save(self, dict):
        return self.table.insert(dict)

    def replace(self, id, dict):
        self.table.update({'_id': ObjectId(id)}, dict, True)

    def remove(self, id):
        self.table.remove({'_id': ObjectId(id)})