# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import time
from colorama import init


LOG_COLOR = {'INFO': '94m', 'ERROR': '31m', 'WARNING': '93m', 'SUCCESS': '92m', 'CRITICAL': '91m'}
TAG_LOG = {'INFO': '*', 'WARNING': '!', 'ERROR': '-', 'SUCCESS': '+', 'CRITICAL': '#'}


init()


class Logging():

    def __init__(self):
        pass

    def log(self, message, level='INFO', bold=False, flush=False):
        """
        Write terminal

        :param message: Text to write in terminal
        :param level: Level text message
        :param bold: Set text is bold
        :param flush: Write on the same line
        :return:
        """

        sys.stdout.write(
            '\033[96m[{time}] \033[{bold}{color}[{tag}] {string}\033[0m{flushed}'.format(
                time=time.strftime("%H:%M:%S"),
                bold='1m\033[' if bold else '',
                color=LOG_COLOR[level],
                tag=TAG_LOG[level],
                string=message,
                flushed='\n' if not flush else '\r'
            )
        )

        sys.stdout.flush()
