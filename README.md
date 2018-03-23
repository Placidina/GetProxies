# GetProxies
![Python 2.7](https://img.shields.io/badge/python-2.7-green.svg)

Free proxy Search

# Screenshot
![Terminal](https://i.imgur.com/znTV1Cg.png)

# Installation
Cloning the [Git](https://github.com/Placidina/GetProxies) repository
````
git clone https://github.com/Placidina/GetProxies.git
````
Install dependencies
```
$ python -m pip install requests gevent lxml argparse
```
GetProxies works out of the box with [Python](http://www.python.org/download/) version 2.7.x on Linux platform.

# Arguments
```
-o | --output         Output list of proxies
--aliveproxy          Get proxies from aliveproxy.com
--checkerproxy        Get proxies from checkerproxy.net
--coolproxy           Get proxies from cool-proxy.net
--freeproxylist       Get proxies from freeproxylists.com
--gatherproxy         Get proxies from gatherproxy.com
--proxyhttp           Get proxies from proxyhttp.net
--proxyiplist         Get proxies from proxy-ip-list.com
--proxynova           Get proxies from proxynova.com
--all                 Get proxies from all sites
--all-no              All proxies except
--check               Verify the proxies is working
```

# Usage
```
./getproxies.py --all
./getproxies.py --aliveproxy
./getproxies.py --aliveproxy --proxynova
./getproxies.py --aliveproxy -o ~/proxies.txt
./getproxies.py --all --all-no=checkerproxy
./getproxies.py --all --all-no=checkerproxy,aliveproxy
```