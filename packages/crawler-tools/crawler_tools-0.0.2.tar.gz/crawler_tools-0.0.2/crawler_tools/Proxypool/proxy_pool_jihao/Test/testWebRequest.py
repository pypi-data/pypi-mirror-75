# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     testWebRequest
   Description :   test class WebRequest
   Author :        J_hao
   date：          2017/7/31
-------------------------------------------------
   Change Activity:
                   2017/7/31: function testWebRequest
-------------------------------------------------
"""
__author__ = 'J_hao'

from Util.WebRequest import WebRequest


# noinspection PyPep8Naming
def testWebRequest():
    """
    test class WebRequest in Util/WebRequest.py
    :return:
    """
    wr = WebRequest()
    url ='www.baidu.com'
    '''修改url作特定测试'''
    print('正在做该 {url}的测试.........................'.format(url = url))
    request_object = wr.get(url)
    assert request_object.status_code == 200


if __name__ == '__main__':
    testWebRequest()
