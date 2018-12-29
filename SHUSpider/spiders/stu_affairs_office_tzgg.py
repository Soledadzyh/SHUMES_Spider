# http://www.xgb.shu.edu.cn/Default.aspx?tabid=31640
# student affairs office
# -*- coding: utf-8 -*-
import datetime
from urllib import parse
import scrapy
from scrapy import Request
import sys

from scrapy.http import HtmlResponse
from selenium import webdriver
from scrapy.selector import Selector

from SHUSpider.settings import TIME_DELTA_DAYS

sys.path.append(r"C:\Users\Amo\PycharmProjects\SHUMES_Spider\SHUSpider")
from SHUSpider.items import NewsItemLoader, NewsItem
from SHUSpider.utils.com import get_md5
from pytime import pytime
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class ShunewsSpider(scrapy.Spider):
    name = 'stu_affairs_office_tzgg'
    allowed_domains = ['xgb.shu.edu.cn']
    start_urls = ["http://www.xgb.shu.edu.cn/Default.aspx?tabid=31640"]
    browser = None
    next_page = None

    def __init__(self):
        self.browser = webdriver.Firefox()
        self.browser.get(self.start_urls[0])
        super(ShunewsSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print("spider closed")
        self.browser.quit()

    def parse(self, response):
        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析

        while response:
            post_nodes = response.css("#dnn_ctr59825_ArticleList__ctl0_ArtDataList a::attr(href)").extract()
            news_time = response.css("#dnn_ctr59825_ArticleList__ctl0_ArtDataList__ctl0_Label6::text").extract_first()
            if pytime.count(pytime.today(), news_time) > datetime.timedelta(TIME_DELTA_DAYS):
                print(news_time + "\n")
                return

            for post_node in post_nodes:
                yield Request(url=parse.urljoin(response.url, post_node), callback=self.parse_detail)

            self.browser.find_element_by_css_selector("#dnn_ctr59825_ArticleList__ctl0_lbtnNext").click()
            selector = Selector(text=self.browser.page_source)
            page_num = selector.css("#dnn_ctr59825_ArticleList__ctl0_plPageNum::text")
            print("page is " + page_num)
            response = HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, encoding="utf-8")

        return

    def parse_detail(self, response):
        # 提取文章中的图片的url
        image_url = response.css(".img_vsb_content::attr(src)").extract()
        image_url_list = [parse.urljoin(response.url, url) for url in image_url]
        # 提取文章具体字段
        # title author webname url create_date content image_url_list tag apartment
        news_item = NewsItem()
        item_loader = NewsItemLoader(item=NewsItem(), response=response)
        # 文章标题
        item_loader.add_css("title", "#dnn_ctr59825_ArtDetail_lblTitle::text")
        # 文章地址
        item_loader.add_value("url", response.url)
        # key：md5_id
        md5_id = get_md5(response.url)
        item_loader.add_value("md5_id", [md5_id])
        # item_loader.add_value("url_object_id", get_md5(response.url))
        # 发布时间
        item_loader.add_css("create_date", "#dnn_ctr59825_ArtDetail_lblDatePosted::text")
        # 图片地址
        item_loader.add_value("image_url_list", image_url_list)
        # 类型标签
        item_loader.add_value("tag", ["通知公告"])
        # item_loader.add_value("tag_id", ["6"])
        # 一级标签：一般为来源(网站名）
        item_loader.add_value("webname", ["学生工作办公室"])
        # 一级标签：一般为来源(网站名）
        # item_loader.add_value("user_id", ["3"])
        # 内容#vsb_content_2
        item_loader.add_css("content",
                            "#dnn_ctr59825_ArtDetail_lblArticle")
        # 部门
        item_loader.add_css("apartment", "#dnn_ctr59825_ArticleDetails_ctl00_hypDept::text")
        # 发布人
        author = response.css("#dnn_ctr59825_ArtDetail_hypFirst::text").extract_first() + response.css(
            "#dnn_ctr59825_ArtDetail_hypLast::text").extract_first()
        item_loader.add_value("author", [author])
        # item_loader.add_css("image_url_list","p.vsbcontent_img img::attr(src)")

        news_item = item_loader.load_item()

        yield news_item
