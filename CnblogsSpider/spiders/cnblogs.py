# -*- coding: utf-8 -*-
from urllib import parse
import json

import scrapy
from scrapy import Request
import requests
import re



class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['www.cnblogs.com/news/']
    start_urls = ['http://www.cnblogs.com/news/']

    def parse(self, response):
        post_nodes = response.css('#post_list  .post_item')
        for post_node in post_nodes:
            image_url = post_node.css('.post_item_summary a img::attr(href)').extract_first("")
            post_url = post_node.css('h3::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)

        # 提取出下一页并交给scrapy去做处理
        # css获取
        next_text = response.css('div.pager a:last-child::text').extract_first("")
        if next_text == "Next >":
            next_url = response.css('div.pager a:last-child::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, next_url))

    def parse_detail(self,  response):
        title = response.css('#news_title a::text').extract_first("")
        publish_time = response.css('#news_info .time::text').extract_first("")
        content = response.css('#news_content').extract("")[0]
        tag_list = response.css('.news_tags a::text').extract()

        match_re=re.match(".*?(\d+)", response.url)
        if match_re:
            post_id = match_re.group(1)
            html = requests.get(parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))
            j_data = json.load(html.text)
            like_nums =j_data["DiggCount"]  # 点赞数
            view_nums = j_data["TotalView"]  # 阅读数
            comment_nums = j_data["CommentCount"]  # 评论数
        pass