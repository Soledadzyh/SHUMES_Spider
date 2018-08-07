# -*- coding: utf-8 -*-
import json

import scrapy

class SzshuSpider(scrapy.Spider):
    name = 'szSHU'
    allowed_domains = ['www.sz.shu.edu.cn']
    start_urls = ['http://www.sz.shu.edu.cn/tongz/ShuZGG.aspx']
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"
    header = {
        "Host": "www.sz.shu.edu.cn",
        "Referer": "http://www.sz.shu.edu.cn/Login.aspx",
        "User-Agent": agent
    }
    def parse(self, response):

        pass

    def start_requests(self):
        return [scrapy.Request("http://www.sz.shu.edu.cn/Login.aspx",headers=self.header,callback=self.login)]


    def login(self,response):
        post_url = "http://www.sz.shu.edu.cn/api/Sys/Users/Login"
        post_data = {
            "userName": "16122847",
            "password": "1234Shu",
        }

        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.header,
            callback=self.check_login
        )]


    def check_login(self,response):
        # 验证服务器的返回数据是否成功
        text_json = json.loads(response.text)
        if "message" in text_json and text_json["message"] == "成功":
            for url in self.start_urls:
                yield scrapy.Request(url,dont_filter=True,headers=self.header)

        pass