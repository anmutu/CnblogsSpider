# -*- coding: utf-8 -*-
from urllib import parse


import scrapy
from scrapy import Request


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['www.cnblogs.com/news/']
    start_urls = ['http://www.cnblogs.com/news/']

    def parse(self, response):
        post_nodes = response.css('#post_list  .post_item')
        for post_node in post_nodes:
            image_url = post_node.css('.post_item_summary a img::attr(href)').exact_first("")
            post_url = post_node.css('h3::attr(href)').exact_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)

        # 提取出下一页并交给scrapy去做处理
        # css获取
        next_text = response.css('div.pager a:last-child::text').extract_first("")
        if next_text == "Next >":
            next_url = response.css('div.pager a:last-child::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, next_url))


    def parse_detail(self, response):
        pass