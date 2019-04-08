# -*- coding: utf-8 -*-

import sys
import requests
import lxml.html

from core import Threading


class AliveProxy():
    """
    aliveproxy.com
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
            'Looking at aliveproxy.com...',
            flush=True
        )

        results = []
        threads = [
            Threading(
                target=self.get,
                args=(
                    'high-anonymity-proxy-list/',
                )
            ),
            Threading(
                target=self.get,
                args=(
                    'anonymous-proxy-list/',
                )
            ),
            Threading(
                target=self.get,
                args=(
                    'transparent-proxy-list/',
                )
            )
        ]

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
        except requests.exceptions.Timeout:
            return result
        except requests.exceptions.TooManyRedirects:
            return result
        except requests.exceptions.RequestException as err:
            self.log(err, 'ERROR', True)
            return result

        tree = lxml.html.fromstring(resp.text)
        for row in tree.findall('.//tr[@class="cw-list"]'):
            proxy, _, _, _, _, _, _, _, _, _ = map(
                lambda x: x.xpath('.//br/preceding-sibling::text()[1]'),
                row.findall('.//td')
            )

            result.append({
                'ip': proxy[0].split(':')[0],
                'port': int(proxy[0].split(':')[1]),
                'ms': None
            })

        return result
