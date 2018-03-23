# -*- coding: utf-8 -*-

import requests
import lxml.html

from thread_manager import ThreadHandler
from requests.exceptions import Timeout, TooManyRedirects, RequestException


class AliveProxyHandler(ThreadHandler):
    """
    Class to get proxies in aliveproxy.com
    """

    def __init__(self, event_log, header):
        super(AliveProxyHandler, self).__init__()
        self.log = event_log
        self.header = header

    def initialize(self):
        """
        Start threads to get proxies

        :return: Array list proxies
        """

        self.log(
            'Looking at aliveproxy.com...',
            flush=True
        )

        results = []
        threads = [
            ThreadHandler(
                target=self.get,
                args=(
                    'high-anonymity-proxy-list/',
                )
            ),
            ThreadHandler(
                target=self.get,
                args=(
                    'anonymous-proxy-list/',
                )
            ),
            ThreadHandler(
                target=self.get,
                args=(
                    'transparent-proxy-list/',
                )
            )
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            results.append(thread.join())

        result = [x for i in results for x in i]

        self.log(
            'Total at aliveproxy.com: \033[93m{}'.format(
                len(result)
            )
        )

        return [x for i in results for x in i]

    def get(self, link):
        """
        Get proxies

        :param link: Link to get proxies
        :return: Array list proxies
        """

        result = []

        try:
            resp = requests.get(
                'http://aliveproxy.com/{}'.format(
                    link
                ),
                headers=self.header
            )
        except Timeout:
            return result
        except TooManyRedirects:
            return result
        except RequestException as err:
            self.event_handler.log(err, 'ERROR', True)
            return result

        tree = lxml.html.fromstring(resp.text)
        for tr in tree.findall('.//tr[@class="cw-list"]'):
            proxy, _, _, _, _, _, _, _, _, _ = map(
                lambda x: x.text_content().strip().replace(' ', '').replace('\t', ''),
                tr.findall('.//td')
            )
            result.append(proxy)

        return result
