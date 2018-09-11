from scrapy.cmdline import  execute
import sys

import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
'''
    分别是新闻网
    成就系统 没有爬 要登陆 然后发现大部分迁移到熟知网
    新闻网中的视频新闻
    图书馆
    本科招生网
'''
# execute(['scrapy','crawl','SHUnews_kydt'])
# execute(['scrapy','crawl','SHUnews_zyxw'])
# execute(['scrapy','crawl','SHUnews_zhxw'])
# execute(['scrapy','crawl','SHUnews_whxx'])
# execute(['scrapy','crawl','szSHU'])
# execute(["scrapy","crawl","spxw"])
# execute(["scrapy","crawl","librarynews"])
execute(["scrapy","crawl","enrolnews"])
