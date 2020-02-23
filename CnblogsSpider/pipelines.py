# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import time

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import MySQLdb
import  MySQLdb.cursors



class CnblogsspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    """
    得到图片的pipline
    """
    def item_completed(self, results, item, info):
        if "front_img_url" in item:
            img_file_path = ""
            for ok, value in results:
                img_file_path = value["path"]
            item["front_img_path"] = img_file_path
        return item


class JsonWithEncodingPipeline(object):
    """
    自定义Json文件的导出(自己写的)
    """
    def __init__(self):
        now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.file = codecs.open('{}{}.json'.format(now, "article"), 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    """
    官方scrapy提供的导出的方法 from scrapy.exporters
    """
    def __init__(self):
        now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.file = open('{}{}.json'.format(now, "article_scrapy"), 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    """
          (这里是同步入库，对于要求较高的来说并不是很友好)
    """
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'cnblogs_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
          insert into article_spider 
          values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        parms = list()
        parms.append(item.get("title", ""))
        parms.append(item.get("url", ""))
        parms.append(item.get("url_id", ""))
        parms.append(item.get("publish_time", ""))
        parms.append(item.get("front_img_path", ""))
        parms.append(item.get("front_img_url", ""))
        parms.append(item.get("like_nums", 0))
        parms.append(item.get("view_nums", 0))
        parms.append(item.get("comment_nums", 0))
        parms.append(item.get("tags", ""))
        parms.append(item.get("content", "1970-07-01"))

        self.cursor.execute( insert_sql, tuple(parms))
        self.conn.commit()
        return item



