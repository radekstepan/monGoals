#!/usr/bin/python
# -*- coding: utf -*-

class Progress:

    logs = None

    def add_log(self, log):
        if self.logs is None:
            self.logs = log
        else:
            self.logs += log

    def sort_log(self, log=None):
        if log is None:
            if self.logs is not None:
                return sorted(self.logs, key=lambda k: k['date'])
        else:
            return sorted(log, key=lambda k: k['date'])
