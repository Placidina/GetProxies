# -*- coding: utf-8 -*-

import sys
import copy
import re
import lxml.html
import requests

from requests.exceptions import Timeout, TooManyRedirects, RequestException
from core import Threading


class GatherProxy():
    """
    gatherproxy.com
    """

    def __init__(self, event_log, header):
        self.log = event_log
        self.header = header

    def initialize(self):
        """
        Start threads to get proxies

        :return: Array list proxies
        """

        self.log(
            'Looking at gatherproxy.com...',
            flush=True
        )

        results = []
        threads = []
        proxy_types = [
            'elite',
            'anonymous',
            'transparent'
        ]

        for proxy_type in proxy_types:
            pages = self.pages(proxy_type)
            pages_per_threads = (pages[i:i + 20] for i in range(0, len(pages), 20))

            for pgs in pages_per_threads:
                threads.append(
                    Threading(
                        target=self.get,
                        args=(
                            proxy_type,
                            pgs,
                        )
                    )
                )

        for thread in threads:
            thread.start()

        try:
            for thread in threads:
                results.append(thread.wait())
        except KeyboardInterrupt:
            self.log('Ctrl-C caught, exiting', 'WARNING', True)
            sys.exit(1)

        result = [x for i in results for x in i]

        self.log(
            'Total at gatherproxy.com: \033[93m{}'.format(
                len(result)
            )
        )

        return result

    def pages(self, proxy_type):
        """
        Get total pages

        :param proxy_type: Proxy type
        :return: Total pages
        """

        headers = copy.copy(self.header)
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        try:
            resp = requests.post(
                'http://www.gatherproxy.com/proxylist/anonymity/?t={}'.format(
                    proxy_type[0].upper() + proxy_type[1:]
                ),
                headers=headers,
                data='Type={}&PageIdx=1&Uptime=0'.format(
                    proxy_type[0].lower() + proxy_type[1:]
                )
            )
        except requests.exceptions.RequestException as err:
            self.log(err, 'ERROR', True)
            return 0

        tree = lxml.html.fromstring(resp.text)
        pagenavi = tree.xpath('.//div[@class="pagenavi"]/a')
        pages = list(map(lambda x: x.text, pagenavi))

        result = []
        for i in range(1, int(pages[-1])):
            result.append(i)

        return result

    def get(self, proxy_type, pages):
        """
        Get proxies

        :param proxy_type: Proxy type
        :param pages: Page to get proxies
        :return: Array list proxies
        """

        result = []

        headers = copy.copy(self.header)
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        for page in pages:
            try:
                resp = requests.post(
                    'http://www.gatherproxy.com/proxylist/anonymity/?t={}'.format(
                        proxy_type[0].upper() + proxy_type[1:]
                    ),
                    headers=headers,
                    data='Type={}&PageIdx={}&Uptime=0'.format(
                        proxy_type[0].lower() + proxy_type[1:],
                        page
                    )
                )
            except Timeout:
                continue
            except TooManyRedirects:
                continue
            except RequestException as err:
                self.log(err, 'ERROR', True)
                continue

            tree = lxml.html.fromstring(resp.text)
            for row in tree.xpath('.//table/tr')[2:]:
                _, ipv4, port, _, _, _, _, _ = map(
                    lambda x: x.text_content().strip().replace(' ', '').replace('\t', ''),
                    row.findall('.//td')
                )

                result.append({
                    'ip': re.search(r'[0-9]+(?:\.[0-9]+){3}', ipv4).group(),
                    'port': int(port.split("'")[1], 16),
                    'ms': None
                })

        return result
