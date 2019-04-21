# -*- coding: utf-8 -*-

# Scrapy settings for SHUSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'SHUSpider'

SPIDER_MODULES = ['SHUSpider.spiders']
NEWSPIDER_MODULE = 'SHUSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'SHUSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
import sys

LOG_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(LOG_DIR, "SHUSpider"))
# print(os.path.join(BASE_DIR,"SHUSpider")
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'SHUSpider.middlewares.ShuspiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'SHUSpider.middlewares.ShuspiderDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'SHUSpider.pipelines.ShuspiderPipeline': 300,
    "SHUSpider.pipelines.ElasticSearchPipeline": 500
    # "SHUSpider.pipelines.MysqlTwistedPipeline":  500
    # "SHUSpider.pipelines.PostgresTwistedPipeline": 500,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# MYSQL_HOST = "101.132.105.112"
# MYSQL_DBNAME = "shumessage"
# MYSQL_USER = "root"
# MYSQL_PASSWORD = "miaoxiaojie"


MYSQL_HOST = "api.mzz.pub"
MYSQL_DBNAME = "message"
MYSQL_USER = "root"
MYSQL_PASSWORD = "Miaoxiaojie123"
"""
    POSTGRES
"""
POSTGRES_HOST = "129.204.71.113"
POSTGRES_DBNAME = "message"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "0ggmr0"

SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"
TIME_DELTA_DAYS = 400

TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhOTVjODljYy1iNjNhLTQzYWEtODk3OC0zYjI4NmQ4NTI5MGIiLCJuaWNrbmFtZSI6IiVFNyU4QyVBQSVFOCVCOSU4NDEiLCJleHAiOjQ3MDkyMzg2MTgsImlhdCI6MTU1NTYzODYxOH0.N21AUkbB9nndkVVrsjYrTe96oDiE8dDUF15SHJyouY4"
