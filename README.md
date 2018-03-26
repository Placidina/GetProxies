# GetProxies
[![Build Status](https://travis-ci.org/Placidina/GetProxies.svg?branch=master)](https://api.travis-ci.org/Placidina/GetProxies) [![Python 2.7](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv3-red.svg)](https://github.com/Placidina/GetProxies/blob/master/LICENSE)

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
$ python -m pip install -r requirements.txt
```
GetProxies works out of the box with [Python](http://www.python.org/download/) version 2.7.x on any platform.

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
python getproxies.py --all
python getproxies.py --aliveproxy
python getproxies.py --aliveproxy --proxynova
python getproxies.py --aliveproxy -o ~/proxies.txt
python getproxies.py --all --all-no=checkerproxy
python getproxies.py --all --all-no=checkerproxy,aliveproxy
```