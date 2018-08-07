# -*- coding: utf-8 -*-
import datetime
from urllib import parse
import scrapy
from scrapy import Request

from SHUSpider.items import NewsItemLoader, NewsItem

# 就业信息服务网
class WorkshuSpider(scrapy.Spider):
    name = 'workSHU'
    allowed_domains = ['zbb.shu.edu.cn']
    start_urls = ['http://zbb.shu.edu.cn/InformationList.aspx?SubInfoType=%E5%85%AC%E7%A4%BA%E5%85%AC%E5%91%8A']

    def parse(self, response):
        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_nodes = response.css(
            ".table tr")

        for post_node in post_nodes:
            post_url = response.css(".table tr")[0].css("a::attr(href)").extract_first()
            if(datetime.datetime.strptime(response.css("#line_u4_0 > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > \
                                                          tr:nth-child(1) > td:nth-child(2) > span:nth-child(1)::text").extract_first(""),"%Y-%m-%d")\
                    > datetime.datetime.strptime('2018-01-01', '%Y-%m-%d')):
                yield Request(url=parse.urljoin(response.url, post_node),callback=self.parse_detail)
            else:
                break

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
        item_loader.add_css("title", "#dnn_ctr1053_ArticleDetails_ctl00_lblTitle::text")
        # 文章地址
        item_loader.add_value("url", response.url)
        # item_loader.add_value("url_object_id", get_md5(response.url))
        # 发布时间
        item_loader.add_css("create_date", "#dnn_ctr1053_ArticleDetails_ctl00_lblDatePosted::text")
        # 图片地址
        item_loader.add_value("image_url_list", image_url_list)
        # 类型标签
        item_loader.add_value("tag", ["媒体关注"])
        # 一级标签：一般为来源(网站名）
        item_loader.add_value("webname", ["新闻网"])
        # 内容#vsb_content_2
        item_loader.add_xpath("content", "//div[@id='vsb_content_2'] | /html/body/div[1]/div[3]/div/table/tbody/tr/td/div/div[2]/div/div/div/form")
        # 部门
        item_loader.add_css("apartment", "#dnn_ctr1053_ArticleDetails_ctl00_hypDept::text")
        # 发布人
        item_loader.add_css("author", "#dnn_ctr1053_ArticleDetails_ctl00_hypUser::text")
        # item_loader.add_css("image_url_list","p.vsbcontent_img img::attr(src)")

        news_item = item_loader.load_item()

        yield news_item

