# -*- coding: utf-8 -*-
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

# 教务处_通知公告
class JwcSpider(scrapy.Spider):
    name = 'jwc_xw'
    allowed_domains = ['jwc.shu.edu.cn']
    start_urls = ['http://www.jwc.shu.edu.cn/index/xw.htm']

    def parse(self, response):
        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_nodes = response.css(
            "#dnn_ctr43516_ArticleList__ctl0_ArtDataList__ctl1_titleLink1::attr(href)").extract()
        news_time = response.css(
            "dnn_ctr43516_ArticleList__ctl0_ArtDataList__ctl1_Label6::text").extract_first()
        if pytime.count(pytime.today(), news_time) > datetime.timedelta(TIME_DELTA_DAYS):
            print(news_time)
            return

        for post_node in post_nodes:
            yield Request(url=parse.urljoin(response.url, post_node), callback=self.parse_detail)

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
        item_loader.add_value("image_url_list", image_url_list)
        # 类型标签
        item_loader.add_value("tag", ["新闻"])
        # item_loader.add_value("tag_id", ["6"])
        # 一级标签：一般为来源(网站名）
        item_loader.add_value("webname", ["教务处"])
        # 一级标签：一般为来源(网站名）
        # item_loader.add_value("user_id", ["3"])
        # 内容#vsb_content
        item_loader.add_css("content", "#vsb_content")
        # 部门
        item_loader.add_css("apartment", "#dnn_ctr1053_ArticleDetails_ctl00_hypDept::text")
        # 发布人
        item_loader.add_css("author", "#dnn_ctr43465_ArtDetail_hypFirst::text")
        # item_loader.add_css("image_url_list","p.vsbcontent_img img::attr(src)")

        news_item = item_loader.load_item()

        yield news_item

