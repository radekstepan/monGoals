#!/usr/bin/python
# -*- coding: utf -*-

# db
from bson.objectid import ObjectId
from db import db

class Goals:

    table = db.goals

    def find_one(self, id):
        return self.table.find_one({"_id": ObjectId(id)})

    def find_all(self):
        return self.table.find()

    def save(self, dict):
        return self.table.insert(dict)