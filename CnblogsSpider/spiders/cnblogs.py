# -*- coding: utf-8 -*-
from urllib import parse, response
import json


import scrapy
from scrapy import Request
import re
from CnblogsSpider.items import CnblogsspiderItem
from CnblogsSpider.util import common


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['www.cnblogs.com/news/']
    start_urls = ['http://www.cnblogs.com/news/']

    def parse(self, response):
        """
        1.获取列表中的url且将之交给scrapy下载，然后交由detail做解析
        2.获取下一页的列表数据，将下一页的数据交给parse处理，也就是做1做的事情。
        """
        post_nodes = response.css('#post_list  .post_item')[:1]
        for post_node in post_nodes:
            image_url = post_node.css('.post_item_summary a img::attr(src)').extract_first("")
            post_url = post_node.css('h3 a::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail, dont_filter=True)

        # 提取出下一页并交给scrapy去做处理
        # next_text = response.css('div.pager a:last-child::text').extract_first("")
        # if next_text == "Next >":
        #     next_url = response.css('div.pager a:last-child::attr(href)').extract_first("")
        #     yield Request(url=parse.urljoin(response.url, next_url))

    def parse_detail(self, response):
        """
        获取详情信息的函数
        """
        article_item = CnblogsspiderItem
        title = response.css('#news_title a::text').extract_first("")
        publish_time = response.css('#news_info .time::text').extract_first("")
        match_re = re.match(".*?(\d+.*)", publish_time)
        if match_re:
            publish_time = match_re.group(1)
        content = response.css('#news_content').extract()[0]
        tag_list = response.css('.news_tags a::text').extract()
        tags = ",".join(tag_list)

        # article_item["title"] = title
        # article_item["publish_time"] = publish_time
        # article_item["content"] = content
        # article_item["tags"] = tags
        # article_item["url"] = response.url
        # if response.meta.get("front_image_url", ""):
        #     article_item["front_img_url"] = [response.meta.get("front_image_url", "")]
        # else:
        #     article_item["front_img_url"] = []

        match_re=re.match(".*?(\d+)", response.url)
        if match_re:
            post_id = match_re.group(1)

            yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)),
                          meta={"article_item": article_item}, callback=self.parse_ajax_data, dont_filter=True)

            # 此处代码换成异步的
            # html = requests.get(parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))
            # j_data = json.load(html.text)
            # like_nums =j_data["DiggCount"]  # 点赞数
            # view_nums = j_data["TotalView"]  # 阅读数
            # comment_nums = j_data["CommentCount"]  # 评论数
        pass

    def parse_ajax_data(self, response):
        """
        详情里有几个数据是ajax请求得到的，不是服务器里的数据，这块也优化成异步取数据
        """
        j_data = json.loads(response.text)
        like_nums =j_data["DiggCount"]  # 点赞数
        view_nums = j_data["TotalView"]  # 阅读数
        comment_nums = j_data["CommentCount"]  # 评论数

        article_item = response.meta.get("article_item")
        article_item["like_nums"] = like_nums
        article_item["view_nums"] = view_nums
        article_item["comment_nums"] = comment_nums
        article_item["url_id"] = common.get_md5(article_item["url"])

        yield article_item

