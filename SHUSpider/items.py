# -*- coding: utf-8 -*-

import datetime

import scrapy
from pytime import pytime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

from SHUSpider.models.es_types import NewsType

'''
后来在数据库中新增了md5_id   
'''


class SHUSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_convert(value):
    # if isinstance(value, str):
    try:
        create_date = pytime.parse(value)
    except Exception as e:
        create_date = datetime.datetime.now().date()
    # else:
    #     create_date = value.date()
    return create_date


def strip_blank(value):
    return value.strip()


class NewsItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class NewsItem(scrapy.Item):
    """md5_id title author webname(user_name) url create_date content image_url_list tag apartment"""
    title = scrapy.Field(
        input_processor=MapCompose(strip_blank)
    )
    author = scrapy.Field()
    webname = scrapy.Field()
    url = scrapy.Field()
    md5_id = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    content = scrapy.Field()
    apartment = scrapy.Field()
    tag = scrapy.Field()

    def get_postgre_sql(self):
        insert_sql_news = """
                   insert into tbl_news(news_name, users_id, news_url, news_content_for_scrapy, 
                   img_url, type, md5, create_time, department)
                   VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE create_date=VALUES (create_date)
               """

        insert_sql_labels = """
                    insert into tbl_news_and_labels(labels_name, news_id, labels_id)
                    VALUES (%s, %s, %s)
        """

        insert_sql_tags = """
                    insert into tbl_labels(labels_name)
                    VALUES (%s)
        """

        params_news = (
            self['title'], self['user_id'], self['url'], self['content'],
            self.get('image_url_list', ''),
            self["md5_id"], self['create_date'],  # self['webname'],
            self.get('apartment', '')
        )

        params_labels = [
            self["labels_name"]
        ]

        return insert_sql_news, insert_sql_labels, insert_sql_tags, params_news, params_labels

    def get_insert_sql(self):
        """
        the former sql
        """

        # insert_sql = """
        #     insert into news(md5_id, title, author, create_date, user_name, url, apartment, tag, content,
        #     image_url_list)
        #     VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE create_date=VALUES (create_date),
        #     image_url_list=VALUES(image_url_list),tag=VALUES(tag),apartment=VALUES (apartment),author=VALUES (author)
        # """
        #
        # params = (
        #     self["md5_id"], self['title'], self.get('author', ''), self['create_date'], self['webname'], self['url'],
        #     self.get('apartment', ''), self['tag'],
        #     self['content'], self.get('image_url_list', '')  # , self['user_id'], self['tag_id']
        # )
        # # params = (
        # #     self["md5_id"], self['title'], self['create_date'], self['webname'], self['url'],
        # #     self['content'], self['user_id'], self['tag_id']
        # # )
        # return insert_sql, params

        """
        the new sql for mysql
        """

        insert_sql_news = """
                   insert into message.tbl_News( md5_id, title, author, 
                                            create_date, user_id, user_name, url,
                                            apartment, tag_id, tag, content,
                                             image_url_list, type)
                   VALUES (%s, %s, %s, 
                   %s, %s, %s, %s, %s, 
                   %s, %s, %s, %s, %s) 
                   ON DUPLICATE KEY UPDATE create_date=VALUES (create_date)
               """

        insert_sql_labels = """
                    insert into tbl_news_and_labels(labels_name,  labels_id, news_id)
                    VALUES (%s, %s, %s)
        """

        # insert_sql_tags = """
        #             insert into tbl_labels(labels_name)
        #             VALUES (%s)
        # """

        params_news = (
            self["md5_id"], self['title'],self.get("author", ""), self['create_date'],
            self['user_id'], self['webname'],
            self['url'], self.get('apartment', ''), self["tag_id"], self["tag"], self['content'],
            self.get('image_url_list', ''), self["type"]
        )

        params_labels = [
            self["tag"], self["tag_id"]
        ]

        # params_users = [
        #     self["webname"]
        # ]

        return insert_sql_news, params_news, insert_sql_labels, params_labels  # , params_users

    def save_to_es(self):
        news = NewsType()
        news.title = self["title"]
        news.create_date = self["create_date"]
        news.content = remove_tags(self["content"])
        news.tag = self["tag"]
        news.meta.id = self["md5_id"]
        news.webname = self["webname"]
        news.url = self["url"]
        news.apartment = self.get("apartment", "")
        news.author = self.get("author", "")
        news.labels = self.get("labels", "")
        news.save()
        return
