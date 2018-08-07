# -*- coding: utf-8 -*-
import datetime
from urllib import parse
import scrapy
from scrapy import Request

from SHUSpider.items import NewsItemLoader, NewsItem

class EnrolnewsSpider(scrapy.Spider):
    name = 'enrolnews'
    allowed_domains = ['bkzsw.shu.edu.cn']
    start_urls = ['http://bkzsw.shu.edu.cn/zsxx/tzgg.htm']


    def parse(self, response):
        nodes = response.css("#dnn_ctr63411_ArticleList__ctl0_ArtDataList>tr")
        for post_node in nodes:
            post_url = post_node.css("a::attr(href)").extract_first()
            create_date = post_node.css("span::text").extract_first()
            if (datetime.datetime.strptime(create_date, "%Y-%m-%d") \
                    > datetime.datetime.strptime('2018-01-01', '%Y-%m-%d')):
                print("TRUE")
                yield Request(url=parse.urljoin(response.url, post_url), meta={"create_date": create_date},
                              callback=self.parse_detail)
            else:
                print("False")
                break
        # 提取下一页并交给scrapy进行下载
        next_url = response.css("a.Next:nth-child(3)::attr(href)").extract_first()
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
        item_loader.add_css("title", "#dnn_ctr63596_ArtDetail_lblTitle::text")
        # 文章地址
        item_loader.add_value("url", response.url)
        # item_loader.add_value("url_object_id", get_md5(response.url))
        # 发布时间
        create_date = response.meta.get("create_date", "")
        item_loader.add_value("create_date", create_date)
        # 图片地址
        item_loader.add_value("image_url_list", image_url_list)
        # 类型标签
        item_loader.add_value("tag", "通知公告")
        # 一级标签：一般为来源(网站名）
        item_loader.add_value("webname", ["本科招生网"])
        # 内容#vsb_content_2
        item_loader.add_css("content", "#vsb_content")
        # 部门
        # item_loader.add_css("apartment", "")
        # 发布人
        item_loader.add_css("author", "#dnn_ctr63596_ArtDetail_hypFirst::text")
        # item_loader.add_css("image_url_list","p.vsbcontent_img img::attr(src)")

        news_item = item_loader.load_item()

        yield news_item
