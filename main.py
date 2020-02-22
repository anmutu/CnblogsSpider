# _*_ coding :utf-8 _*_
__author__ = 'du'
__bolg__ = 'www.github.com/anmutu;'
__date__ = '2020/2/19 22:44'

from scrapy.cmdline import execute
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", "crawl", "cnblogs"])
# execute(["scrapy", "crawl", "scenario"])