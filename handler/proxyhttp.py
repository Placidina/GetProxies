# -*- coding: utf-8 -*-

import sys
import re
import lxml.html
import requests

from requests.exceptions import Timeout, TooManyRedirects, RequestException
from core import Threading


class ProxyHTTP():
    """
    proxyhttp.net
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
            'Looking at proxyhttp.net...',
            flush=True
        )

        results = []
        threads = []

        pages = self.pages()
        for page in pages:
            threads.append(
                Threading(
                    target=self.get,
                    args=(
                        page,
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
            'Total at proxyhttp.net: \033[93m{}'.format(
                len(result)
            )
        )

        return result

    def pages(self):
        """
        Get pages

        :return: Array pages
        """

        result = []

        try:
            resp = requests.get(
                'http://proxyhttp.net/free-list/anonymous-server-hide-ip-address/1',
                headers=self.header
            )
        except Timeout:
            return result
        except TooManyRedirects:
            return result
        except RequestException as err:
            self.log(err, 'ERROR', True)
            return result

        tree = lxml.html.fromstring(resp.text)
        pages = list(map(lambda x: x.text, tree.findall('.//div[@id="pages"]/a')))

        for page in range(1, int(pages[-2])):
            result.append(page)

        return result

    def get(self, page):
        """
        Get proxies

        :param page: Page to get proxies
        :return: Array list proxies
        """

        result = []

        try:
            resp = requests.get(
                'http://proxyhttp.net/free-list/anonymous-server-hide-ip-address/{}'.format(
                    page
                ),
                headers=self.header
            )
        except Timeout:
            return result
        except TooManyRedirects:
            return result
        except RequestException as err:
            self.log(err, 'ERROR', True)
            return result

        tree = lxml.html.fromstring(resp.text)

        javascript = tree.xpath(
            './/script[contains(text(),"<![CDATA")]'
        )[0].text.replace('\n', '').replace(' ', '').replace('//', '')
        javascript = re.search(r'CDATA\[(.*)\]\]', javascript).group(1)
        exec(javascript)

        for row in tree.xpath('.//table[@class="proxytbl"]/tr')[1:]:
            ipv4, port, _, _, _, _, _ = map(
                lambda x: x.text_content().strip().replace(' ', '').replace('\t', ''),
                row.findall('.//td')
            )

            script = port.replace('\n', '').replace(' ', '').replace('//', '')
            script = re.search(r'CDATA\[document\.write\((.*)\)\;\]\]', script).group(1)

            result.append({
                'ip': ipv4,
                'port': int(eval(script)),
                'ms': None
            })

        return result
