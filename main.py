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
# 新闻网
# execute(['scrapy','crawl','SHUnews'])
# 熟知网
# execute(['scrapy','crawl','szSHU'])

# execute(["scrapy","crawl","librarynews"])

# 本科招生网
execute(["scrapy","crawl","enrolnews"])

# 教务处 通知公告 新闻

# execute(["scrapy","crawl","jwc"])

# 学工办
# execute(["scrapy","crawl","stu_affairs_office"])