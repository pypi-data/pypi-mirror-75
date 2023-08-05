# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
import os
from  threading import Thread as td


def proxy_schedule():
    """启动代理爬取"""
    print('请确认代理池启动准备工作------redis数据库启动成功....................................')
    start = input('1:已经准备完成.................;2:准备未完成，前往准备中................\n')

    if int(start) == 1:
        print('进入启动界面..................................')
        proxy_module = input('输入需要启动的代理池模块： 输入命令格式为——1（崔）or2（jihao) \n')
        if int(proxy_module) == 1:
            print('代理池cui启动中.............................................................')
            os.system('python {}\\proxy_pool_cui\\run.py'.format(os.path.abspath(os.path.dirname(__file__))))
        elif int(proxy_module) == 2:
            print('代理池jihao启动中.............................................................')

            def schedule():
                os.system('python {}\\proxy_pool_jihao\\Schedule\\ProxyScheduler.py'.format(
                    os.path.abspath(os.path.dirname(__file__))))

            def api():
                os.system(
                    'python {}\\proxy_pool_jihao\\Api\\ProxyApi.py'.format(os.path.abspath(os.path.dirname(__file__))))

            thread = []
            thread.append(td(target=schedule))
            thread.append(td(target=api))
            # & F:\\PyCharm项目\\常用设置\\Proxypool\\proxy_pool_jihao\\Api\\ProxyApi.py')
            print(thread)
            if __name__ == '__main__':
                for t in thread:
                    t.start()
            print('................................................................................')
    else:
        print('退出中...............................')
        exit(0)

#proxy_schedule()