# -*- coding: utf-8 -*-

import sys
import lxml.html
import requests

from requests.exceptions import Timeout, TooManyRedirects, RequestException
from core import Threading


class ProxyNova():
    """
    proxynova.com
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
            'Looking at proxynova.com...',
            flush=True
        )

        results = []
        threads = []

        countries = self.countries()
        countries_per_threads = (countries[i:i + 30] for i in range(0, len(countries), 30))

        for cts in countries_per_threads:
            threads.append(
                Threading(
                    target=self.get,
                    args=(
                        cts,
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
        results = list(map(
            lambda x: x.attrib['value'] if x.attrib.has_key('value') and x.attrib['value'] else None,
            tree.findall('.//select[@name="proxy_country"]/option')
        ))

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
            for row in tree.xpath('.//table[@id="tbl_proxy_list"]/tbody/tr'):
                column = row.findall('.//td')
                if len(column) == 8:
                    ipv4, port, _, _, _, _, _, _ = map(lambda x: x, column)
                    result.append({
                        'ip': ipv4.find('.//abbr').attrib['title'].strip().replace(' ', '').replace('\t', ''),
                        'port': int(port.text_content().strip().replace(' ', '').replace('\t', '')),
                        'ms': None
                    })

        return result
