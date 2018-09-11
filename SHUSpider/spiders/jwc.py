# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import datetime
from urllib import parse
import scrapy
from scrapy import Request

from SHUSpider.items import NewsItemLoader, NewsItem
from SHUSpider.utils.com import get_md5

# 教务处
class JwcSpider(CrawlSpider):
    name = 'jwc'
    allowed_domains = ['jwc.shu.edu.cn']
    start_urls = ['http://www.jwc.shu.edu.cn/Default.aspx?tabid=22970']

    rules = (
        Rule(LinkExtractor(allow=r'/Default.aspx?tabid=((23168)|(22970))&ctl=Detail(.*)'), callback='parse_zzxw', follow=True),
    )
    # 通知新闻
    def parse_tzzx(self, response):
        i = {}
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
        create_date = response.meta.get("create_date", "")
        item_loader.add_value("create_date", create_date)
        # 图片地址
        item_loader.add_value("image_url_list", image_url_list)
        # 类型标签
        item_loader.add_css("tag",
                            "div.field:nth-child(2) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)::text")
        # 一级标签：一般为来源(网站名）
        item_loader.add_value("webname", ["图书馆"])
        # 内容#vsb_content_2
        item_loader.add_css("content",
                            "div.field:nth-child(1)")
        news_item = item_loader.load_item()

        return i
