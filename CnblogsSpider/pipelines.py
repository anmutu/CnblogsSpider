# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline

class CnblogsspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipleline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_img_url" in item:
            for ok, value in results:
                img_file_path = value["path"]
            item["front_img_path"] = img_file_path
        return item