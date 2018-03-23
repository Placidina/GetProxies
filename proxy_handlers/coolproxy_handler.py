# -*- coding: utf-8 -*-

import base64
import codecs
import lxml.html
import re
import requests

from thread_manager import ThreadHandler
from requests.exceptions import Timeout, TooManyRedirects, RequestException


class CoolProxyHandler(ThreadHandler):
    """
    Class to get proxies in cool-proxy.net
    """

    def __init__(self, event_log, header):
        super(CoolProxyHandler, self).__init__()
        self.log = event_log
        self.header = header

    def initialize(self):
        """
        Start threads to get proxies

        :return: Array list proxies
        """

        self.log(
            'Looking at cool-proxy.net...',
            flush=True
        )

        results = []
        threads = []

        pages = self.pages()
        pages_per_threads = (pages[i:i + 3] for i in xrange(0, len(pages), 3))
        for pgs in pages_per_threads:
            threads.append(
                ThreadHandler(
                    target=self.get,
                    args=(
                        pgs,
                    )
                )
            )

        for thread in threads:
            thread.start()

        for thread in threads:
            results.append(thread.join())

        result = [x for i in results for x in i]

        self.log(
            'Total at cool-proxy.net: \033[93m{}'.format(
                len(result)
            )
        )

        return result

    def pages(self):
        """
        Get total pages

        :return: Array list pages
        """

        try:
            resp = requests.get(
                'https://www.cool-proxy.net/proxies/http_proxy_list/page:1/sort:score/direction:desc',
                headers=self.header
            )
        except Timeout:
            return 0
        except TooManyRedirects:
            return 0
        except RequestException as err:
            self.log(err, 'ERROR', True)
            return 0

        tree = lxml.html.fromstring(resp.text)
        th = tree.find('.//th[@class="pagination"]')
        pages = map(lambda x: x.text_content(), th.findall('.//a'))

        result = []
        for page in xrange(1, int(pages[-2])):
            result.append(page)

        return result

    def get(self, pages):
        """
        Get proxies

        :param page: Page to get proxies
        :return: Array list proxies
        """

        result = []

        for page in pages:
            try:
                resp = requests.get(
                    'https://www.cool-proxy.net/proxies/http_proxy_list/page:{}/sort:score/direction:desc'.format(
                        page
                    )
                )
            except Timeout:
                return result
            except TooManyRedirects:
                return result
            except RequestException as err:
                self.log(err, 'ERROR', True)
                return result

            tree = lxml.html.fromstring(resp.text)
            for tr in tree.xpath('.//table/tr')[1:]:
                td = tr.findall('.//td')
                if len(td) == 10:
                    ip, port, _, _, _, _, _, _, _, _ = map(
                        lambda x: x.text_content().strip().replace(' ', '').replace('\t', ''),
                        td
                    )
                    result.append('{}:{}'.format(
                        base64.decodestring(
                            codecs.getdecoder('rot13')(
                                re.search('"(.*)"', ip).group(1)
                            )[0]
                        ),
                        port)
                    )

        return result
