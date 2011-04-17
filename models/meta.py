#!/usr/bin/python
# -*- coding: utf -*-

import utils

class Meta:

    def from_log(self, log):
        '''calculate the progress past today, 7 days, 30 days'''
        for entry in log:
            p = entry['points']['points']
            if entry['date'] > self.meta['today']['current']['cutoff']:
                self.meta['today']['current']['points'] += p
                self.meta['seven']['current']['points'] += p
                self.meta['thirty']['current']['points'] += p
            else:
                if entry['date'] > self.meta['today']['previous']['cutoff']:
                    self.meta['today']['previous']['points'] += p
                    self.meta['seven']['current']['points'] += p
                    self.meta['thirty']['current']['points'] += p
                else:
                    if entry['date'] > self.meta['seven']['current']['cutoff']:
                        self.meta['seven']['current']['points'] += p
                        self.meta['thirty']['current']['points'] += p
                    else:
                        if entry['date'] > self.meta['seven']['previous']['cutoff']:
                            self.meta['seven']['previous']['points'] += p
                            self.meta['thirty']['current']['points'] += p
                        else:
                            if entry['date'] > self.meta['thirty']['current']['cutoff']:
                                self.meta['thirty']['current']['points'] += p
                            elif entry['date'] > self.meta['thirty']['previous']['cutoff']:
                                self.meta['thirty']['previous']['points'] += p
        return self.meta

    def __init__(self):
        now = utils.timestamp_new()
        self.meta = {
            'now': now,
            'today': {
                'current': {
                    'cutoff': now - (60*60*24),
                    'points': 0
                },
                'previous': {
                    'cutoff': now - (60*60*24*2),
                    'points': 0
                },
            },
            'seven': {
                'current': {
                    'cutoff': now - (60*60*24*7),
                    'points': 0
                },
                'previous': {
                    'cutoff': now - (60*60*24*7*2),
                    'points': 0
                },
            },
            'thirty': {
                'current': {
                    'cutoff': now - (60*60*24*30),
                    'points': 0
                },
                'previous': {
                    'cutoff': now - (60*60*24*30*2),
                    'points': 0
                },
            },
        }