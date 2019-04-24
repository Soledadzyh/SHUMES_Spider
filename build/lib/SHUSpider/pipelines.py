# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import datetime
import json
import os
import grequests, requests
import scrapy
from pytime import pytime
from scrapy.exporters import JsonItemExporter
import pymysql, psycopg2
from scrapy.http import HtmlResponse
from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem
from w3lib.html import remove_tags

from SHUSpider.settings import TIME_DELTA_DAYS, URL, HEADERS


class ShuspiderPipeline(object):
    def process_item(self, item, spider):
        if pytime.count(pytime.today(), item['create_date']) < datetime.timedelta(TIME_DELTA_DAYS):
            return item


# class MysqlPipeline(object):
#     #采用同步的机制写入mysql
#     def __init__(self):
#         self.conn = pymysql.connect('localhost', 'root', '123456', 'shumessage', charset="utf8", use_unicode=True)
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         insert_sql = """
#             insert into news(title, author, create_date, webname, url,apartment, tag, content,image_url_list)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(content),title=VALUES (title),
#             author=VALUES (author),create_date=VALUES (create_date),webname=VALUES (webname),url=VALUES (url),
#             tag=VALUES (tag),image_url_list=VALUES (image_url_list),apartment=VALUES (apartment)
#         """
#         self.cursor.execute(insert_sql, (item['title'], item['author'], item['create_date'], item['webname'], item['url'],item['apartment'], item['tag'],
#              item['content'], item['image_url_list']))
#         self.conn.commit()

"""
    pipeline中只有MysqlTwistedPipeline在使用中
    异步导入数据库
    其他格式的pipeline只是拿来练手的
"""

"""
POSTGRES
"""
#
# class PostgresTwistedPipeline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         dbparms = dict(
#             host=settings['POSTGRES_HOST'],
#             password=settings["POSTGRES_PASSWORD"],
#             cursorclass=pymysql.cursors.DictCursor,
#             database=settings["POSTGRES_DBNAME"],
#             user=settings["POSTGRES_USER"]
#         )
#         dbpool = adbapi.ConnectionPool("psycopg2", **dbparms)
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         # 使用twisted将mysql插入变成异步执行
#         query = self.dbpool.runInteraction(self.do_insert, item)
#         query.addErrback(self.handle_error, item, spider)  # 处理异常
#
#     def handle_error(self, failure, item, spider):
#         print(failure)
#
#     def do_insert(self, cursor, item):
#         # 执行具体的插入
#         insert_sql_news, insert_sql_labels, insert_sql_tags,  params_news, params_labels = item.get_postgre_sql()
#         try:
#             cursor.execute(insert_sql_news, params_news)
#
#         news_id = int(cursor.lastrowid)
#         cursor.execute(insert_sql_tags, params_labels)
#         news_id = int(cursor.lastrowid)
#         params_labels.append(news_id)
#         cursor.execute(insert_sql_labels, params_labels)
#         psycopg2.connect()

"""
MYSQL
"""


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            password=settings["MYSQL_PASSWORD"],
            cursorclass=pymysql.cursors.DictCursor,
            database=settings["MYSQL_DBNAME"],
            charset='utf8mb4',
            user=settings["MYSQL_USER"]
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addCallback(self.add_label_news, item, spider)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql_news, params_news, insert_sql_labels, params_labels = item.get_insert_sql()
        cursor.execute(insert_sql_news, params_news)
        # try:
        #     cursor.execute(insert_sql_labels, params_labels)
        #     label_id = cursor.fetchall()[0][0]
        #     params_labels.append(label_id)
        # except:
        #     pass
        # except Exception as e:
        #     pass


# userId	发布新闻的官方账号的uuid String
# mediaTitle	爬取的新闻的标题 String
# newsUrl	爬取的新闻的url String
# newsLabelId	新闻标签的uuid（周总爬虫爬下来的时候是自带标签的） String
# contentFromScrapy	爬取的新闻的内容，供做分析的同学拿去使用 String
# md5	周总说这个是用来确认爬取的新闻是唯一的，详细情况请咨询周总 String
# createTime	爬取的新闻发布的时间，格式为 1998-02-04 12:12:12
#
# title author webname  url  md5_id  create_date content apartment  tag
# POST JSON to postgresql
class POSTJsonPipeline(object):
    def __init__(self):
        self.ids = json.load(open("SHUSpider/tools/tag_web_ids.json"))

    def process_item(self, item, spider):
        d_item = dict(item)
        new_item = {}
        new_item["md5"] = d_item["md5_id"]
        new_item["userId"] = self.ids[(d_item["webname"])]
        new_item["mediaTitle"] = d_item["title"]
        new_item["newsUrl"] = d_item["url"]
        new_item["newsLabelId"] = self.ids[d_item["tag"]]
        new_item["contentFromScrapy"] = d_item["content"]
        new_item["createTime"] = str(d_item["create_date"])+" 00:00:00"
        lines = json.dumps(new_item, ensure_ascii=False) + '\n'
        resp = requests.request(method="POST", url=URL + "/news", headers=HEADERS, data =lines.encode("utf-8"))

        print(resp.text)
        # print(grequests.map(resp).text())
        return item


# 自定义的json导出
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open("news.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        d_item = dict(item)
        d_item["md5"] = d_item["md5_id"]

        post_js = dict(item).pop(["author", "apartment", "md5_id"])
        lines = json.dumps(post_js, ensure_ascii=False) + '\n'

        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


# 使用Jsonexporter
class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open("newsexporter.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ElasticSearchPipeline(object):
    # 将数据导入es中
    def process_item(self, item, spider):
        # 将items中的数据放入es
        item.save_to_es()
        return item


project_dir = os.path.abspath(os.path.dirname(__file__))
