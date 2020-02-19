# -*- coding: utf-8 -*-
import scrapy


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['www.cnblogs.com/news/']
    start_urls = ['http://www.cnblogs.com/news/']

    def parse(self, response):
        pass
