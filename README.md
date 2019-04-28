# GetProxies

[![CircleCI](https://img.shields.io/circleci/project/github/Placidina/GetProxies.svg?style=popout-square")](https://circleci.com/gh/Placidina/GetProxies)
[![Python 3.7](https://img.shields.io/badge/python-3.7-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-GPLv3-red.svg)](https://github.com/Placidina/GetProxies/blob/master/LICENSE)

Bot to search free HTTP proxies

## Screenshot

![Terminal](https://i.imgur.com/znTV1Cg.png)

## Installation

Cloning the [Git](https://github.com/Placidina/GetProxies) repository
````
git clone https://github.com/Placidina/GetProxies.git
````

Install dependencies
```
$ python -m pip install -r requirements.txt
```

GetProxies works out of the box with [Python](http://www.python.org/download/) version 3.x on any platform.

## Output

Output JSON result
```
[
    {
        "ip": "127.0.0.1",
        "port": 3128,
        "ms": null
    },
    ...
]
```

* Parameter `ip` of type `String` - IP of proxy
* Parameter `port` of type `Integir` - Port of proxy
* Parameter `ms` of type `null` or `String` - Proxy response time of argument `--check`

## Arguments

```
-o | --output         Output JSON file (e.g, exemple.json)
--aliveproxy          Get proxies from aliveproxy.com
--checkerproxy        Get proxies from checkerproxy.net
--freeproxylist       Get proxies from freeproxylists.com
--gatherproxy         Get proxies from gatherproxy.com
--proxyhttp           Get proxies from proxyhttp.net
--proxyiplist         Get proxies from proxy-ip-list.com
--proxynova           Get proxies from proxynova.com
--all                 Get proxies from all sites
--all-no              All proxies except
--check               Verify the proxies is working
--check-url CHECKER   Url to checke your current ip
```

## Usage

```
python getproxies.py --all
python getproxies.py --aliveproxy
python getproxies.py --aliveproxy --proxynova
python getproxies.py --aliveproxy -o ~/proxies.json
python getproxies.py --all --all-no=checkerproxy
python getproxies.py --all --all-no=checkerproxy,aliveproxy
```