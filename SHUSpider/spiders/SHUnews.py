# -*- coding: utf-8 -*-
import datetime
from urllib import parse
import scrapy
from scrapy import Request
import sys

from SHUSpider.settings import TIME_DELTA_DAYS

sys.path.append(r"C:\Users\Amo\PycharmProjects\SHUMES_Spider\SHUSpider")
from SHUSpider.items import NewsItemLoader, NewsItem
from SHUSpider.utils.com import get_md5
from pytime import pytime


class ShunewsSpider(scrapy.Spider):
    name = 'SHUnews'
    allowed_domains = ['news.shu.edu.cn']
    start_urls = ["http://news.shu.edu.cn/index/kydt.htm",  # 科研动态
                  "http://news.shu.edu.cn/index/zyxw.htm",  # 重要新闻
                  "http://news.shu.edu.cn/index/zhxw.htm",  # 综合新闻
                  "http://news.shu.edu.cn/index/whxx.htm",  # 文化信息
                  "http://news.shu.edu.cn/index/tpxw.htm",  # 图片新闻
                  "http://news.shu.edu.cn/index/spxw.htm"
                  ]

    def parse(self, response):
        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析//*[@id="dnn_dnnBREADCRUMB_lblBreadCrumb"]/a[2]
        tag = response.css("#dnn_dnnBREADCRUMB_lblBreadCrumb > a:nth-child(2)::text").extract_first()
        post_nodes = response.css(
            "#dnn_ctr1053_ArticleList_ctl00_lstArticles > tbody:nth-child(1) a::attr(href)").extract()
        news_time = response.css(
            "#dnn_ctr1053_ArticleList_ctl00_lstArticles_ctl00_lblPublishDate::text").extract_first()
        if pytime.count(pytime.today(), news_time) > datetime.timedelta(TIME_DELTA_DAYS):
            print(news_time)
            return

        for post_node in post_nodes:
            yield Request(url=parse.urljoin(response.url, post_node),  meta ={"tag": tag}, callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        next_url = response.css("a.Next:nth-child(3)::attr(href)").extract_first("")

        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        # 提取文章中的图片的url
        image_url = response.css("p.vsbcontent_img img::attr(src)").extract()
        image_url_list = [parse.urljoin(response.url, url) for url in image_url]
        # 提取文章具体字段
        # title author webname url create_date content image_url_list tag apartment
        news_item = NewsItem()
        item_loader = NewsItemLoader(item=NewsItem(), response=response)
        # 文章标题
        item_loader.add_xpath("title",'//*[@id="dnn_ctr1055_ArticleDetails_ctl00_lblTitle"]/text()|//*['
                                      '@id="dnn_ctr1053_ArticleDetails_ctl00_lblTitle"]/text()')
        # 文章地址
        item_loader.add_value("url", response.url)
        # key：md5_id
        md5_id = get_md5(response.url)
        item_loader.add_value("md5_id", [md5_id])
        # item_loader.add_value("url_object_id", get_md5(response.url))
        # 发布时间 //*[@id="dnn_ctr1053_ArticleDetails_ctl00_lblDatePosted"]
        item_loader.add_xpath("create_date",
                              "//*[@id='dnn_ctr1053_ArticleDetails_ctl00_lblDatePosted']/text()| //*["
                              "@id='dnn_ctr1055_ArticleDetails_ctl00_lblDatePosted']/text()")
        # 类型标签

        item_loader.add_value("tag", response.meta.get("tag",""))
        # 一级标签：一般为来源(网站名）
        item_loader.add_value("webname", ["新闻网"])
        # 一级标签：一般为来源(网站名）
        # 内容#vsb_content_2   //*[@id="dnn_ctr43465_ModuleContent"]
        item_loader.add_css("content","[id*='vsb_content']")
        # #vsb_content_503
        # 部门
        item_loader.add_xpath("apartment",
                              "//*[@id='dnn_ctr1053_ArticleDetails_ctl00_hypDept']/text()| //*["
                              "@id='dnn_ctr1055_ArticleDetails_ctl00_hypDept']/text()")
        # 发布人
        item_loader.add_xpath("author",
                              "//*[@id='dnn_ctr1053_ArticleDetails_ctl00_hypUser']/text()| //*["
                              "@id='dnn_ctr1055_ArticleDetails_ctl00_hypUser']/text()")
        # item_loader.add_css("image_url_list","p.vsbcontent_img img::attr(src)")

        news_item = item_loader.load_item()

        yield news_item
