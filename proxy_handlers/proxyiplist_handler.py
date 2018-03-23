# -*- coding: utf-8 -*-

import requests
import lxml.html

from thread_manager import ThreadHandler
from requests.exceptions import Timeout, TooManyRedirects, RequestException


class ProxyIPListHandler(ThreadHandler):
    """
    Class to get proxies in proxy-ip-list.com
    """

    def __init__(self, event_log, header):
        super(ProxyIPListHandler, self).__init__()
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

        thread = ThreadHandler(
            target=self.get
        )
        thread.start()
        result = thread.join()

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
        for tr in tree.findall('.//tbody/tr'):
            proxy, _, _, _, _ = map(
                lambda x: x.text_content().strip().replace(' ', '').replace('\t', ''),
                tr.findall('.//td')
            )
            result.append(proxy)

        return result
