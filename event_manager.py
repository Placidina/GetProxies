# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import time
import sys

'''
PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'
'''

COLOR_HEX = {
    'RED': '91m',
    'YELLOW': '93m',
    'GREEN': '92m',
    'BLUE': '94m',
    'CYAN': '96m'
}
LOG_COLOR = {
    'INFO': 'BLUE',
    'ERROR': 'RED',
    'WARNING': 'YELLOW',
    'YES': 'GREEN',
    'NO': 'RED'
}
TAG_LOG = {
    'INFO': '*',
    'WARNING': '!',
    'ERROR': '#',
    'YES': '+',
    'NO': '-'
}


class EventHandler(object):

    def __init__(self):
        self.initialize()

    def log(self, message, level='INFO', bold=False, flush=False):
        if bold:
            sys.stdout.write(
                '\033[96m[{time}] \033[1m\033[{color}[{tag}] {string}\033[0m'.format(
                    time=time.strftime("%H:%M:%S"),
                    color=COLOR_HEX[LOG_COLOR[level]],
                    tag=TAG_LOG[level],
                    string=message
                ) + ('\n' if not flush else '\r')
            )
        else:
            sys.stdout.write(
                '\033[96m[{time}] \033[{color}[{tag}] {string}\033[0m'.format(
                    time=time.strftime("%H:%M:%S"),
                    color=COLOR_HEX[LOG_COLOR[level]],
                    tag=TAG_LOG[level],
                    string=message
                ) + ('\n' if not flush else '\r')
            )

        if flush:
            sys.stdout.flush()

    def initialize(self):
        self.log(
            'GetProxies Initialized'
        )
