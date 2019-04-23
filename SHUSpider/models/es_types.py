from datetime import datetime

import scrapy
from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text

from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["http://112.74.175.228:9200"])


class NewsType(Document):
    title = Text(analyzer="ik_max_word")
    author = Text(analyzer="ik_max_word")
    webname = Text(analyzer="ik_max_word")
    url = Keyword()
    create_date = Date()
    content = Text(analyzer="ik_max_word")
    apartment = Text(analyzer="ik_max_word")
    tag = Text(analyzer="ik_max_word")
    labels = Text(analyzer="ik_max_word")

    class Index:
        name = "news"
        settings = {
            "number_of_shards": 5,
        }


if __name__ == "__main__":
    NewsType.init()
