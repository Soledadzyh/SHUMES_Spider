import re
from datetime import datetime
import json

import pymysql
import requests
from twisted.enterprise import adbapi

from SHUSpider import settings
from SHUSpider.settings import SQL_DATE_FORMAT

r = requests.get("http://www.sz.shu.edu.cn/api/TongZGG/TongZGG/GetXiaoJTZGG?tongzjb=0&pageSize=20&pageNumber=1")
text = r.json()
newsurl = "http://www.sz.shu.edu.cn/tongz/TongZGGInfo.aspx?id="
con = pymysql.connect(
    host=settings.MYSQL_HOST,
    password=settings.MYSQL_PASSWORD,
    cursorclass=pymysql.cursors.DictCursor,
    database=settings.MYSQL_DBNAME,
    charset='utf8',
    user=settings.MYSQL_USER
)
def str_date(str):

    return datetime.strptime(re.match("(.*?)T", str).group(1), SQL_DATE_FORMAT) if str else datetime.date()


for news in text["data"]["tongzgg"]:
    title = news["BiaoTi"]
    webname = "熟知网"
    url = newsurl+ str(news["Id"])
    create_date = str_date(news["CreatedOn"])
    content = news["NeiRong"]
    with con.cursor() as cursor:
        sql = """
            insert into news(title,create_date, webname, url, content)
            VALUES (%s, %s, %s, %s, %s) 
        """
        cursor.execute(sql, (title,create_date, webname, url, content))
    con.commit()
