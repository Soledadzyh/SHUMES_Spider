# -*- coding: utf-8 -*-

import datetime

import scrapy
from pytime import pytime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

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
    # tag_id = scrapy.Field()
    image_url_list = scrapy.Field(
        output_processor=Join("|")
    )

    # user_id = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
            insert into news(md5_id, title, author, create_date, user_name, url, apartment, tag, content, 
            image_url_list)
            VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE create_date=VALUES (create_date),
            image_url_list=VALUES(image_url_list),tag=VALUES(tag),apartment=VALUES (apartment),author=VALUES (author)
        """

        params = (
            self["md5_id"], self['title'], self.get('author', ''), self['create_date'], self['webname'], self['url'],
            self.get('apartment', ''), self['tag'],
            self['content'], self.get('image_url_list', '')  # , self['user_id'], self['tag_id']
        )
        # params = (
        #     self["md5_id"], self['title'], self['create_date'], self['webname'], self['url'],
        #     self['content'], self['user_id'], self['tag_id']
        # )
        return insert_sql, params
