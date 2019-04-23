# -*- coding: utf-8 -*-
import datetime
from urllib import parse
import scrapy
from pytime import pytime
from scrapy import Request

from SHUSpider.items import NewsItemLoader, NewsItem
from SHUSpider.settings import TIME_DELTA_DAYS
from SHUSpider.utils.com import get_md5
import pymysql, psycopg2


class ShunewsSpider(scrapy.Spider):
    name = 'librarynews'
    allowed_domains = ['lib.shu.edu.cn']
    start_urls = [
        'http://www.lib.shu.edu.cn/newsfb',
        "http://www.lib.shu.edu.cn/resourcesfb",
        "http://www.lib.shu.edu.cn/jzxxfb"
    ]

    def parse(self, response):
        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_nodes = response.css(".views-table > tbody:nth-child(1) tr")
        for post_node in post_nodes:
            create_date = post_node.css(".views-field-created::text").extract_first().strip()
            post_node_url = post_node.css("a::attr(href)").extract_first()
            yield Request(url=parse.urljoin(response.url, post_node_url), meta={"create_date": create_date},
                          callback=self.parse_detail, dont_filter=True)
            if pytime.count(pytime.today(), create_date) > datetime.timedelta(TIME_DELTA_DAYS):
                return

        next_url = response.css(".pager-next a::attr(href)").extract_first("")

        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        # 提取文章中的图片的url
        image_url = response.css(".content img::attr(src)").extract()
        image_url_list = [parse.urljoin(response.url, url) for url in image_url]
        # 提取文章具体字段
        # title author webname url create_date content image_url_list tag apartment
        news_item = NewsItem()
        item_loader = NewsItemLoader(item=NewsItem(), response=response)
        # 文章标题 需要处理空格
        item_loader.add_css("title", "#page-title::text")
        # 文章地址
        item_loader.add_value("url", response.url)
        # key：md5_id
        md5_id = get_md5(response.url)
        item_loader.add_value("md5_id", [md5_id])
        # item_loader.add_value("url_object_id", get_md5(response.url))
        # 发布时间
        item_loader.add_value("create_date", response.meta.get("create_date", ""))
        # 图片地址
        # 类型标签
        tag = response.css("div.field:nth-child(2) >"
                           " div:nth-child(1) > div:nth-child(1) > a:nth-child(1)::text").extract_first()
        item_loader.add_value("tag", tag)
        # 一级标签：一般为来源(网站名）
        item_loader.add_value("webname", ["图书馆"])
        # 内容#vsb_content_2
        item_loader.add_css("content",
                            "div.field:nth-child(1)")
        news_item = item_loader.load_item()

        yield news_item
