import codecs
import hashlib
import json

import requests
import scrapy

from SHUSpider.settings import HEADERS, URL, PIC


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


class get_id(object):
    def __init__(self, api, data_name):
        self.api = api
        self.data_name = data_name
        self.data = None
        self.post_data = {
            self.data_name: None
        }
        self.ids = {}
        self.ids = json.load(open("tag_web_ids.json"))


    def check_data(self, response):
        text_json = json.loads(response.text)
        print(text_json["message"])
        if text_json["code"] == 200:
            data_id = text_json["data"]["id"]
            return data_id
        else:
            print(text_json["message"])

    def get_id(self, data):
        self.data = data
        self.post_data={
            self.data_name: self.data
        }
        if self.api=="/user":
            self.post_data["avatar"]=PIC
            print(self.post_data)
        response = requests.request("POST", URL + self.api, data=json.dumps(self.post_data), headers=HEADERS)
        return self.check_data(response)

    def store_id(self, data):
        dict = {data: self.get_id(data)}
        if self.data not in self.ids:
            self.ids[data]=dict[data]
        else:
            print(str(dict) + " already stored")
        return self.ids
