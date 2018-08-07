# -*- coding: utf-8 -*-
import scrapy


class NewsMtgzSpider(scrapy.Spider):
    name = 'news_mtgz'
    allowed_domains = ['http://news.shu.edu.cn/index/mtgz.htm']
    start_urls = ['http://http://news.shu.edu.cn/index/mtgz.htm/']

    def parse(self, response):
        pass
