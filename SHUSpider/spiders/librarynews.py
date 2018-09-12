# -*- coding: utf-8 -*-
import datetime
from urllib import parse
import scrapy
from scrapy import Request

from SHUSpider.items import NewsItemLoader, NewsItem
from SHUSpider.utils.com import get_md5


class ShunewsSpider(scrapy.Spider):
    name = 'librarynews'
    allowed_domains = ['lib.shu.edu.cn']
    start_urls = ['http://www.lib.shu.edu.cn/newsfb',
                  "http://www.lib.shu.edu.cn/resourcesfb",
                  "http://www.lib.shu.edu.cn/jzxxfb"
                  ]

    def parse(self, response):
        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_nodes = response.css(".views-table > tbody:nth-child(1) tr")
        # time response.css(".views-table > tbody:nth-child(1) tr")[0].css(".views-field-created::text").extract()
        # url
        for post_node in post_nodes:
            create_date = post_node.css(".views-field-created::text").extract_first().strip().replace("17-",
                                                                                                      "2017-").replace(
                "18-", "2018-")
            create_date = datetime.datetime.strptime(create_date, "%Y-%m-%d")
            # response.css(".views-table > tbody:nth-child(1) tr")[0].css("a::attr(href)")
            post_node_url = post_node.css("a::attr(href)").extract_first()
            print(create_date > datetime.datetime.strptime('2018-01-01', '%Y-%m-%d'))
            if create_date > datetime.datetime.strptime('2018-01-01', '%Y-%m-%d'):
                yield Request(url=parse.urljoin(response.url, post_node_url), meta={"create_date": create_date},
                              callback=self.parse_detail)
            else:
                break

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
        create_date = response.meta.get("create_date", "")
        item_loader.add_value("create_date", create_date)
        # 图片地址
        item_loader.add_value("image_url_list", image_url_list)
        # 类型标签
        tag = response.css("div.field:nth-child(2) >"
                           " div:nth-child(1) > div:nth-child(1) > a:nth-child(1)::text").extract_first()
        item_loader.add_value("tag", tag)
        tag_num = {"资源动态": "1",
                   "公告信息": "4",
                   "图书馆新闻": "3"}
        item_loader.add_value("tag_id", tag_num[tag])
        # 一级标签：一般为来源(网站名）
        item_loader.add_value("webname", ["图书馆"])
        item_loader.add_value("user_id",["1"])
        # 内容#vsb_content_2
        item_loader.add_css("content",
                            "div.field:nth-child(1)")
        news_item = item_loader.load_item()

        yield news_item
