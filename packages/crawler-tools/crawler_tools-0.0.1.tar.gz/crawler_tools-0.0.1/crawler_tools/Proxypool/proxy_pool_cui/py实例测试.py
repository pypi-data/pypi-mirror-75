# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
from pyquery import PyQuery as pq
import re
from schemas.proxy import Proxy

def Proxy_ceshi():
    doc = pq('http://www.xsdaili.com/dayProxy/ip/2075.html')
    print(type(doc))
    trs = doc('.cont')
    print(type(trs))
    pattern = re.compile(r'<br/>(.*?)@HTTP', re.S)
    results = re.findall(pattern,str(trs))
    for result in results:
        print(type(result))
        host=result.split(':')[0]
        port = int(result.split(":")[1])
        print(host,port)
        yield Proxy(host,port)
for porxt in Proxy_ceshi():
    print(porxt)

    #proxy = ('proxy',result.strip().split(':'))

    #print(proxy)