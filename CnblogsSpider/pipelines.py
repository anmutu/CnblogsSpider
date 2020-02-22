# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import datetime

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter


class CnblogsspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipleline(ImagesPipeline):
    """
    得到图片的pipline
    """
    def item_completed(self, results, item, info):
        if "front_img_url" in item:
            for ok, value in results:
                img_file_path = value["path"]
            item["front_img_path"] = img_file_path
        return item


class JsonWithEncodingPipeline(object):
    """
    自定义Json文件的导出(自己写的)
    """
    def __init__(self):
        self.file = codecs.open('mydefined.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipleline(object):
    """
    官方scrapy提供的导出的方法 from scrapy.exporters
    """
    def __init__(self):
        self.file = open('office.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item