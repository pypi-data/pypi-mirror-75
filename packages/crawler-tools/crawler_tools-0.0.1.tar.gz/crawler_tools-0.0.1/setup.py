"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm

from setuptools import setup, find_packages

setup(
    # pip install nnn
    name="crawler_tools",
    version="0.0.1",
    keywords=("crawler", "tools", "proxy","cookies","user-agent"),
    description="语音控制",
    long_description="爬虫工具集合，其中代理用的是崔庆才的代理池和jhao的代理池，而cookies和user-agent是自己的创作，总体上实在综合",
    # 协议
    license="GPL Licence",

    url="",
    author="cw",
    author_email="1063117365@qq.com",

    # 自动查询所有"__init__.py"
    python_requires = '>=3.7.*',
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    # 提示前置包
    install_requires=['selenium',
                      'requests',
                      'APScheduler',
                      'werkzeug==0.15.3',
                      'Flask',
                      'lxml',
                      'PyExecJS',
                      'click',
                      'gunicorn==19.9.0',
                      'redis',
                      'environs==7.2.0',
                      'attrs',
                      'retrying',
                      'aiohttp==3.6.2',
                      'loguru==0.3.2',
                      'pyquery',
                      'supervisor',
                      ]
)
#"speech_recognition"3.8.1需要这个包，但是pip install speak_command时不行，只能用的时候自行下载