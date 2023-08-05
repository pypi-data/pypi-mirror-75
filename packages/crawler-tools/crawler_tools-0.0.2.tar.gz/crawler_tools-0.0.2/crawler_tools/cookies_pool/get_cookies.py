# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
import os,sys
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as options
import random
#print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from user_agent import user_agent as u

PORXY_POOL_URL = 'http://localhost:5555/random'


class Cookies():
    def __init__(self,url):
        self.url = url
        headers = {'User - Agent':u.user_agent()["User-Agent"],'Connection': 'close'}
        self.headers = headers

    def requests_cookies(self):
        cookies = []

        for i in range(2):
            r = requests.get(self.url, headers=self.headers)

            cookies.append(r.cookies.get_dict())
        #print(cookies)
        return cookies
        #requests的cookies不是可以直接传入的字典格式



    def firefox_cookies(self):
        """速度比较慢"""
        cookies = []
        for i in range(2):
            opt = options()#注意options并不是通用的，chrome与firefox需要自行导入
            opt.add_argument('--headless')
            browser = webdriver.Firefox(options=opt)
            #参数不要重复不能as options
            browser.get(self.url)
            cookies.append(browser.get_cookies())
            browser.close()
        return cookies

    #return导致break

    def cookies_random(self):
        cookies = self.requests_cookies()+self.firefox_cookies()
        #print(cookies)
        path = os.path.abspath(os.path.dirname(__file__))+'\\cookies.txt'
        with open(path, 'w', encoding='utf-8')as f:
            f.write(str(cookies))
            f.close()
            print('cookies 存储完毕........................')
        with open(path)as f:
            cookie = f.read().replace("[","").replace("]","")
            cookies = eval(cookie)#字符串元组化
            #print(random.choice(cookies))
            return random.choice(cookies)






