# -*- coding: utf-8 -*-

import sys
import lxml.html
import requests

from requests.exceptions import Timeout, TooManyRedirects, RequestException
from core import Threading


class ProxyIPList():
    """
    proxy-ip-list.com
    """

    def __init__(self, event_log, header):
        self.log = event_log
        self.header = header

    def initialize(self):
        """
        Start thread to get proxies

        :return: Array list proxies
        """

        self.log(
            'Looking at proxy-ip-list.com...',
            flush=True
        )

        thread = Threading(target=self.get)
        thread.start()

        try:
            result = thread.wait()
        except KeyboardInterrupt:
            self.log('Ctrl-C caught, exiting', 'WARNING', True)
            sys.exit(1)

        self.log(
            'Total at proxy-ip-list.com: \033[93m{}'.format(
                len(result)
            )
        )

        return result

    def get(self):
        """
        Get proxies

        :return: Array list proxies
        """
        result = []

        try:
            resp = requests.get(
                'http://proxy-ip-list.com',
                headers=self.header
            )
        except Timeout:
            return result
        except TooManyRedirects:
            return result
        except RequestException as err:
            self.log.log(err, 'ERROR', True)
            return result

        tree = lxml.html.fromstring(resp.text)
        for row in tree.findall('.//tbody/tr'):
            proxy, _, _, _, _ = map(
                lambda x: x.text_content().strip().replace(' ', '').replace('\t', ''),
                row.findall('.//td')
            )

            result.append({
                'ip': proxy.split(':')[0],
                'port': int(proxy.split(':')[1]),
                'ms': None
            })

        return result
