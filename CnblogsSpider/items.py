# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CnblogsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    publish_time = scrapy.Field()
    url = scrapy.Field()
    url_id = scrapy.Field()
    front_img_url = scrapy.Field()
    front_img_path = scrapy.Field()
    like_nums = scrapy.Field()
    view_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    tags = scrapy.Field()
    contents = scrapy.Field()
    pass
