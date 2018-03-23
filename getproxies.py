#!/usr/bin/env python2

import sys
import re
import argparse
import requests

from gevent import monkey
from event_manager import EventHandler
from thread_manager import ThreadHandler
from proxy_handlers import GatherProxyHandler, ProxyIPListHandler, AliveProxyHandler,\
CoolProxyHandler, ProxyNovaHandler, ProxyHTTPHandler, CheckerProxyHandler, FreeProxyListHandler

monkey.patch_all()
sys.tracebacklimit = 0


def parse_args():
    """
    Creating an ArgumentParser
    """

    parser = argparse.ArgumentParser(
        description='Free proxy Search'
    )
    group = parser.add_mutually_exclusive_group(
        required=True
    )

    parser.add_argument(
        '-o',
        '--output',
        default='proxies.dat',
        nargs='*',
        help='Output list of proxies.'
    )
    group.add_argument(
        '--aliveproxy',
        default=False,
        action='store_true',
        help='Get proxies from aliveproxy.com'
    )
    group.add_argument(
        '--checkerproxy',
        default=False,
        action='store_true',
        help='Get proxies from checkerproxy.net'
    )
    group.add_argument(
        '--coolproxy',
        default=False,
        action='store_true',
        help='Get proxies from cool-proxy.net'
    )
    group.add_argument(
        '--freeproxylist',
        default=False,
        action='store_true',
        help='Get proxies from freeproxylists.com'
    )
    group.add_argument(
        '--gatherproxy',
        default=False,
        action='store_true',
        help='Get proxies from gatherproxy.com'
    )
    group.add_argument(
        '--proxyhttp',
        default=False,
        action='store_true',
        help='Get proxies from proxyhttp.net'
    )
    group.add_argument(
        '--proxyiplist',
        default=False,
        action='store_true',
        help='Get proxies from proxy-ip-list.com'
    )
    group.add_argument(
        '--proxynova',
        default=False,
        action='store_true',
        help='Get proxies from proxynova.com'
    )
    group.add_argument(
        '--all',
        default=False,
        action='store_true',
        help='Get proxies from all sites'
    )
    parser.add_argument(
        '--all-no',
        default=[],
        help='All proxies except'
    )
    parser.add_argument(
        '--check',
        default=False,
        action='store_true',
        help='Verify the proxies is working'
    )

    return parser.parse_args()


class GetProxies(EventHandler):

    def __init__(self, args):
        super(GetProxies, self).__init__()
        self.save_file_name = args.output
        self.aliveproxy = args.aliveproxy
        self.checkerproxy = args.checkerproxy
        self.coolproxy = args.coolproxy
        self.freeproxylist = args.freeproxylist
        self.gatherproxy = args.gatherproxy
        self.proxyhttp = args.proxyhttp
        self.proxyiplist = args.proxyiplist
        self.proxynova = args.proxynova
        self.all = args.all
        self.all_no = args.all_no
        self.check_proxies = args.check
        self.proxies = []
        self.headers = {
            'User-Agent': 'Mozilla/5.Mozilla/5.0 (Windows NT 10.0; WOW64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
        }
        self.errors = []
        self.total = 0
        self.current_ip = self.get_current_ip()

    def get_current_ip(self):
        """Obtain the current IP"""

        req = requests.get('http://checkip.amazonaws.com', headers=self.headers)
        return req.text.replace('\n', '')

    def run(self):
        """
        Start class GetProxies
        """

        self.log(
            'Your Current IP: \033[93m{}'.format(
                self.current_ip
            )
        )

        all_no = []
        if len(self.all_no):
            all_no = map(str, self.all_no.split(','))

        if self.gatherproxy or self.all and 'gatherproxy' not in all_no:
            self.proxies.append(
                GatherProxyHandler(
                    self.log,
                    self.headers
                ).initialize()
            )

        if self.proxyiplist or self.all and 'proxyiplist' not in all_no:
            self.proxies.append(
                ProxyIPListHandler(
                    self.log,
                    self.headers
                ).initialize()
            )

        if self.aliveproxy or self.all and 'aliveproxy' not in all_no:
            self.proxies.append(
                AliveProxyHandler(
                    self.log,
                    self.headers
                ).initialize()
            )

        if self.coolproxy or self.all and 'coolproxy' not in all_no:
            self.proxies.append(
                CoolProxyHandler(
                    self.log,
                    self.headers
                ).initialize()
            )

        if self.proxynova or self.all and 'proxynova' not in all_no:
            self.proxies.append(
                ProxyNovaHandler(
                    self.log,
                    self.headers
                ).initialize()
            )

        if self.proxyhttp or self.all and 'proxyhttp' not in all_no:
            self.proxies.append(
                ProxyHTTPHandler(
                    self.log,
                    self.headers
                ).initialize()
            )

        if self.checkerproxy or self.all and 'checkerproxy' not in all_no:
            self.proxies.append(
                CheckerProxyHandler(
                    self.log,
                    self.headers
                ).initialize()
            )

        if self.freeproxylist or self.all and 'freeproxylist' not in all_no:
            self.proxies.append(
                FreeProxyListHandler(
                    self.log,
                    self.headers
                ).initialize()
            )

        self.proxies = [ips for proxy_site in self.proxies for ips in proxy_site]
        self.proxies = list(set(self.proxies))

        self.log(
            'Total Unic Proxies Find: \033[93m{}'.format(
                len(self.proxies)
            )
        )

        if self.check_proxies:
            self.log('Testing Proxies...')
            self.start_proxy_checker()
        else:
            self.log('Saving Proxies...')
            for proxy in self.proxies:
                self.save_proxy(proxy)

    def start_proxy_checker(self):
        """
        Start threads to check proxies

        :return:
        """

        threads = []
        if len(self.proxies) >= 100:
            proxies = (
                self.proxies[i:i + len(self.proxies) / 100]
                for i in xrange(0, len(self.proxies), len(self.proxies) / 100)
            )
        else:
            proxies = (
                self.proxies[i:i + len(self.proxies) / 10]
                for i in xrange(0, len(self.proxies), len(self.proxies) / 10)
            )

        for pxs in proxies:
            threads.append(
                ThreadHandler(
                    target=self.checker,
                    args=(
                        pxs,
                    )
                )
            )

        for thread in threads:
            thread.start()

        try:
            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            self.log('Ctrl-C caught, exiting', 'WARNING', True)
            sys.exit(1)

        self.log('Total Working Proxies: \033[93m{}'.format(self.total))

    def checker(self, proxies):
        """
        Check proxy is functional
        """

        for proxy in proxies:
            try:
                resp = requests.get('http://checkip.amazonaws.com',
                                    headers=self.headers,
                                    proxies={
                                        'http': proxy,
                                        'https': proxy
                                    },
                                    timeout=15)
            except:
                continue

            if resp.status_code == 200:
                ip_checked = self.ip_check(resp.text)
                if ip_checked:
                    self.save_proxy(proxy)
                    self.total += 1
                    self.log('Checking Proxy \033[93m{}'.format(proxy), 'YES')

    def ip_check(self, html):
        """
        Verifies that the IP received on self.test_proxy is the same as the proxy
        """

        html_lines = html.splitlines()
        leng = len(html_lines)
        ip_re = '(?:[0-9]{1,3}\.){3}[0-9]{1,3}'

        if leng == 1:
            match = re.match(ip_re, html)
            if match:
                if self.current_ip in html:
                    return False
            else:
                return False
        else:
            return False

        return True

    def save_proxy(self, proxy):
        """Saves the proxies that are functional"""
        
        with open(self.save_file_name, "a") as file_proxy:
            file_proxy.write("%s\n" % proxy)


start = GetProxies(parse_args())
start.run()
