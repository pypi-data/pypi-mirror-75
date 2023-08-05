"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import time
import requests



def get_proxy_cui(url):
    global proxies
    try:
        PORXY_POOL_URL = 'http://localhost:5555/random'
        r = requests.get(PORXY_POOL_URL)
        if r.status_code == 200:
            proxies = {'http': 'http://' + r.text,'https': 'https://' + r.text,}
            '''proxies必须是字典类型——-—— 否则报错：no_proxy = proxies.get('no_proxy') if proxies is not None else NoneAttributeError: 'set' object has no attribute 'get' '''
    except ConnectionError:
        return None
    index = 1
    try:
        while True:
            r = requests.get(url, proxies=proxies)
            if r.status_code == 200:
                print('返回可用代理，以下为抓取的url.....................................................................')
                return proxies
            else:
                continue
    except requests.exceptions.ConnectionError:
        pass
        time.sleep(10)

def get_proxy_jhao(url):
    global proxies
    try:
        """返回对自己爬取网站有用的代理"""
        html = requests.get("http://127.0.0.1:5010/get/").json()
        # print(html)
        proxy = html['proxy']
        proxies = {'http': 'http://' + proxy, 'https': 'https://' + proxy}
    except:
        pass
    index = 1
    try:
        while True:
            r = requests.get(url,proxies = proxies)
            if r.status_code == 200:
                print('返回可用代理，以下为抓取的url.....................................................................')
                return proxies
            else:
                continue
    except requests.exceptions.ConnectionError:
        pass
        time.sleep(10)

