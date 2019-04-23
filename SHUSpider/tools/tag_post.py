"""
tags && userid post to get labelid and userid
"""
# import json
import codecs

from SHUSpider.settings import HEADERS
import scrapy
import json

from SHUSpider.utils.com import get_id

with open("tags_webname.json", 'r') as load_f:
    data = json.load(load_f)


def get_ids():
    # 所有的tags
    a, b =get_id("/label", "labelName"),get_id("/user", "nickname")
    ids, idss={},{}
    for tag in data["tags"]:
        ids = a.store_id(data=tag)

    # 所有的webname对应的userid
    for webname in data["webname"]:
        idss =  b.store_id(data=webname)
    ids.update(idss)
    lines = json.dumps(ids, ensure_ascii=False) + '\n'
    file = codecs.open("tag_web_ids.json", "w", encoding="utf-8")
    file.write(lines)
    print(lines + "store success")
    file.close()



if __name__ == "__main__":
    get_ids()
