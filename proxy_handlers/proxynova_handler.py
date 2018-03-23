# -*- coding: utf-8 -*-

import requests
import lxml.html

from thread_manager import ThreadHandler
from requests.exceptions import Timeout, TooManyRedirects, RequestException


class ProxyNovaHandler(ThreadHandler):
    """
    Class to get proxies in proxynova.com
    """

    def __init__(self, event_log, header):
        super(ProxyNovaHandler, self).__init__()
        self.log = event_log
        self.header = header

    def initialize(self):
        """
        Start thread to get proxies

        :return: Array list proxies
        """

        self.log(
            'Looking at proxynova.com...',
            flush=True
        )

        results = []
        threads = []

        countries = self.countries()
        countries_per_threads = (countries[i:i + 30] for i in xrange(0, len(countries), 30))

        for cts in countries_per_threads:
            threads.append(
                ThreadHandler(
                    target=self.get,
                    args=(
                        cts,
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
            'Total at proxynova.com: \033[93m{}'.format(
                len(result)
            )
        )

        return result

    def countries(self):
        """
        Get countries

        :return: Array list countries
        """

        result = []

        try:
            resp = requests.get(
                'https://www.proxynova.com/proxy-server-list/'
            )
        except Timeout:
            return result
        except TooManyRedirects:
            return result
        except RequestException as err:
            self.log(err, 'ERROR', True)
            return result

        tree = lxml.html.fromstring(resp.text)
        results = map(
            lambda x: x.attrib['value'] if x.attrib.has_key('value') and x.attrib['value'] else None,
            tree.findall('.//select[@name="proxy_country"]/option')
        )

        for country in results[2:]:
            result.append(country)

        return result

    def get(self, countries):
        """
        Get proxies

        :param countries: List countries
        :return: Array list proxies
        """

        result = []

        for country in countries:
            try:
                resp = requests.get(
                    'https://www.proxynova.com/proxy-server-list/country-{}'.format(
                        country
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
            for tr in tree.xpath('.//table[@id="tbl_proxy_list"]/tbody/tr'):
                td = tr.findall('.//td')
                if len(td) == 8:
                    ip, port, _, _, _, _, _, _ = map(lambda x: x, td)
                    result.append('{}:{}'.format(
                        ip.find('.//abbr').attrib['title'].strip().replace(' ', '').replace('\t', ''),
                        port.text_content().strip().replace(' ', '').replace('\t', ''))
                    )

        return result
