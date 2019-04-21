# -*- coding: utf-8 -*-

import requests

import http.cookiejar as cookielib


agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0"
header = {
    "Host": "www.sz.shu.edu.cn",
    "Referer": "http://www.sz.shu.edu.cn/Login.aspx",
    "User-Agent": agent
}

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")

try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未能加载")


def get_index():
    response = session.get("http://www.sz.shu.edu.cn/person.aspx", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
        print("ok")


def is_login():
    person_url = "http://www.sz.shu.edu.cn/person.aspx"
    response = session.get(person_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True


def sz_sys_login(account, password):
    post_url = "http://www.sz.shu.edu.cn/api/Sys/Users/Login"
    post_data = {
        "userName": account,
        "password": password,
    }
    response_text = session.post(post_url, data=post_data, headers=header)
    session.cookies.save(ignore_expires=True, ignore_discard=True)


# sz_sys_login("16122847", "1234Shu")
# is_login()