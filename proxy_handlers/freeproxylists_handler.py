# -*- coding: utf-8 -*-

import codecs
import lxml.html
import requests

from thread_manager import ThreadHandler
from requests.exceptions import Timeout, TooManyRedirects, RequestException


class FreeProxyListHandler(ThreadHandler):
    """
    Class to get proxies in freeproxylists.com
    """

    def __init__(self, event_log, header):
        super(FreeProxyListHandler, self).__init__()
        self.log = event_log
        self.header = header

    def initialize(self):
        """
        Start threads to get proxies

        :return: Array list proxies
        """

        self.log(
            'Looking at freeproxylists.com...',
            flush=True
        )

        results = []
        pages = [
            'elite.html',
            'anonymous.html',
            'non-anonymous.html',
            'https.html',
            'standard.html',
            'us.html',
            'uk.html',
            'ca.html',
            'fr.html'
        ]

        for page in pages:
            threads = []

            links = self.pages(page)
            links_per_threads = (links[i:i + 5] for i in xrange(0, len(links), 5))
            for lks in links_per_threads:
                threads.append(
                    ThreadHandler(
                        target=self.get,
                        args=(
                            lks,
                        )
                    )
                )

            for thread in threads:
                thread.start()

            for thread in threads:
                results.append(
                    thread.join()
                )

        result = [x for i in results for x in i]

        self.log(
            'Total at freeproxylists.com: \033[93m{}'.format(
                len(result)
            )
        )

        return result

    def pages(self, page):
        """
        Get pages to read proxies

        :return: Array pages links
        """

        result = []

        try:
            resp = requests.get(
                'http://www.freeproxylists.com/{}'.format(
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
        for tr in tree.xpath('.//table[@style="font-family:Tahoma;font-size:8.5pt;width:468px;color:#006699;"]/tr')[1:]:
            link, _, _, _ = map(lambda x: x, tr.findall('.//td'))
            real_link = link[0].attrib['href'].split('/')
            result.append(
                'load_{}_{}'.format(
                    real_link[0],
                    real_link[1]
                )
            )

        return result

    def get(self, pages):
        """
        Get Proxies

        :param pages: Pages get proxies
        :return: Array list proxies
        """

        result = []

        for page in pages:
            try:
                resp = requests.get(
                    'http://www.freeproxylists.com/{}'.format(
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

            enc = lxml.html.fromstring(codecs.encode(resp.text, 'utf-8'))
            html = lxml.html.etree.HTML(enc.text_content())
            html_str = lxml.html.etree.tostring(html, pretty_print=True, method="html")
            tree_ = lxml.html.fromstring(html_str)

            for tr_ in tree_.xpath('.//table/tr')[2:]:
                ip, port = map(
                    lambda x: x.text_content().strip().replace(' ', '').replace('\t', ''),
                    tr_.findall('.//td')
                )
                result.append('{}:{}'.format(ip, port))

        return result
