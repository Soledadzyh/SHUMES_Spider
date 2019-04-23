# -*- coding: utf-8 -*-

"""
教务处_通知公告
"""


import scrapy
from pytime import pytime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import datetime
from urllib import parse
import scrapy
from scrapy import Request

from SHUSpider.items import NewsItemLoader, NewsItem
from SHUSpider.settings import TIME_DELTA_DAYS
from SHUSpider.utils.com import get_md5

class JwcSpider(scrapy.Spider):
    name = 'jwc'
    allowed_domains = ['jwc.shu.edu.cn']
    start_urls = ['http://www.jwc.shu.edu.cn/index/tzgg.htm','http://www.jwc.shu.edu.cn/index/xw.htm']

    def parse(self, response):
        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析
        tag = response.css("[style='background-color:#69a6d3; color:#333; font-size:20px']::text").extract_first("")
        post_nodes = response.css(
            "#dnn_ctr43516_ArticleList__ctl0_ArtDataList__ctl1_titleLink1::attr(href)").extract()
        news_time = response.css(
            "dnn_ctr43516_ArticleList__ctl0_ArtDataList__ctl1_Label6::text").extract_first()

        if pytime.count(pytime.today(), news_time) > datetime.timedelta(TIME_DELTA_DAYS):
            print(news_time)
            return

        for post_node in post_nodes:
            yield Request(url=parse.urljoin(response.url, post_node),meta ={"tag":tag}, callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        next_url = response.css("a.Next:nth-child(3)::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        # 提取文章中的图片的url
        image_url = response.css(".img_vsb_content::attr(src)").extract()
        image_url_list = [parse.urljoin(response.url, url) for url in image_url]
        # 提取文章具体字段
        # title author webname url create_date content image_url_list tag apartment
        news_item = NewsItem()
        item_loader = NewsItemLoader(item=NewsItem(), response=response)
        # 文章标题
        item_loader.add_css("title", "#dnn_ctr43465_ArtDetail_lblTitle::text")
        # 文章地址
        item_loader.add_value("url", response.url)
        # key：md5_id
        md5_id = get_md5(response.url)
        item_loader.add_value("md5_id", [md5_id])
        # item_loader.add_value("url_object_id", get_md5(response.url))
        # 发布时间
        item_loader.add_css("create_date", "#dnn_ctr43465_ArtDetail_lblDatePosted::text")
        # 图片地址
        # 类型标签
        item_loader.add_value("tag", response.meta.get("tag",""))
        # 一级标签：一般为来源(网站名）
        item_loader.add_value("webname", ["教务处"])
        # 一级标签：一般为来源(网站名）
        # 内容#vsb_content [id*='vsb_content']

        item_loader.add_css("content","[id*='vsb_content']")
        # 部门
        item_loader.add_css("apartment", "#dnn_ctr1053_ArticleDetails_ctl00_hypDept::text")
        # 发布人
        item_loader.add_css("author", "#dnn_ctr43465_ArtDetail_hypFirst::text")

        news_item = item_loader.load_item()

        yield news_item

