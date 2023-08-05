# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
from crawlers.base import BaseCrawler
from schemas.proxy import Proxy
import re
from pyquery import PyQuery as pq

MAX_PAGE = 100
BASE_URL = 'http://www.xsdaili.com/dayProxy/ip/{page}.html'


class XsdailiCrawler(BaseCrawler):

    urls = [BASE_URL.format(page=page) for page in range(2000, MAX_PAGE + 1)]

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        #print(type(doc))
        trs = doc('.cont')
        #print(type(trs))
        pattern = re.compile(r'<br/>(.*?)@HTTP', re.S)
        results = re.findall(pattern, str(trs))
        for result in results:
            host = result.split(':')[0]
            port = int(result.split(":")[1])
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = XsdailiCrawler()
    for proxy in crawler.crawl():
        print('测试----------中')
        print(proxy)
