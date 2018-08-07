# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime

import scrapy
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
    if isinstance(value,str):
        try:
            create_date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
    else:
        create_date = value.date()
    return create_date


def strip_blank(value):
    return value.strip()


class NewsItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class NewsItem(scrapy.Item):
    """md5_id title author webname url create_date content image_url_list tag apartment"""
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
    image_url_list = scrapy.Field(
        output_processor=Join("|")
    )

    def get_insert_sql(self):
        insert_sql = """
            insert into news_test(md5_id,title, author, create_date, webname, url,apartment, tag, content,image_url_list)
            VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        params = (
            self["md5_id"],self['title'], self.get('author',''), self['create_date'], self['webname'], self['url'], self.get('apartment',''), self['tag'],
            self['content'],  self.get('image_url_list','')
        )
        return insert_sql, params
