from datetime import datetime

import scrapy
from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text

from elasticsearch_dsl.connections import connections

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

connections.create_connection(hosts=["http://112.74.175.228:9200"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=("lowercase"))


class NewsType(Document):
    suggest = Completion(analyzer=ik_analyzer)
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
        name = "new_news"
        settings = {
            "number_of_shards": 5,
        }


if __name__ == "__main__":
    NewsType.init()
