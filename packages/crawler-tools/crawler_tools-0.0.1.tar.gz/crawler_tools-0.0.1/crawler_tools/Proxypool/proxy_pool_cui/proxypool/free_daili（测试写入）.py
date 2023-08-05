# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
import requests
import lxml
from bs4 import BeautifulSoup
import re
import pymongo




class FreeCrawler():

    def __init__(self):
        self.headers ={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }

    def get_page(self,number):
        url = 'http://www.xsdaili.com/dayProxy/ip/' + str(number) + '.html'
        r = requests.get(url,headers=self.headers)
    #print((r.status_code))
        return r.text

    def parse(self,html):
        soup = BeautifulSoup(html,'lxml')
        results = soup.find('div',attrs={'class':'cont'})
        #print(type(results))
    #类型错误了<class 'bs4.element.Tag'>
        #print(results)
        pattern = re.compile(r'<br/>(.*?)@HTTP', re.S)
        result = re.findall(pattern,str(results))
        #print(result)
        for proxy in result:
            proxy = ''.join(proxy.strip())
            yield proxy
    #for result in results:
        #print(result)
    '''def store_shop(self):
        number = 2070
        for i in range(1):
            number = number + i
            html = self.get_page(number)
            client = pymongo.MongoClient('localhost')
            db = client['daili']
            collection = db['daili']
            collection.insert(self.parse(html))
            '''

if __name__ =='__main__':
    crawler = FreeCrawler()
    html = crawler.get_page(2075)
    for proxy in crawler.parse(html):
        print(proxy)









