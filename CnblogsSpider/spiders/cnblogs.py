# -*- coding: utf-8 -*-
import scrapy


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['new.cnblogs.com']
    start_urls = ['http://new.cnblogs.com/']

    def parse(self, response):
        pass
