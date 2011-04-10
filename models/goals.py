#!/usr/bin/python
# -*- coding: utf -*-

# db
from db import db

class Goals:

    table = db.goals

    def find_one(self, id):
        self.table.find_one({"_id": id})

    def find_all(self):
        return self.table.find()

    def save(self, dict):
        return self.table.insert(dict)