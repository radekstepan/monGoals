#!/usr/bin/python
# -*- coding: utf -*-

from copy import deepcopy
import utils

class Progress:

    logs = None

    def add_log(self, log):
        if self.logs is None:
            self.logs = deepcopy(log)
        else:
            self.logs += deepcopy(log)

    def sort_log(self, log=None):
        if log is None:
            if self.logs is not None:
                return utils.sort_list(self.logs)
        else:
            return utils.sort_list(log)
