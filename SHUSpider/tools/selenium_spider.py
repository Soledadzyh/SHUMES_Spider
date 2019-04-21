from selenium import webdriver
from scrapy.selector import Selector
browser = webdriver.Firefox()

browser.get("http://www.xgb.shu.edu.cn/Default.aspx?tabid=31640")

# dnn_ctr59825_ArticleList__ctl0_lbtnNext

browser.find_element_by_css_selector("#dnn_ctr59825_ArticleList__ctl0_lbtnNext").click()

browser.find_element_by_css_selector("#dnn_ctr59825_ArticleList__ctl0_lbtnNext").click()

selector = Selector(text=browser.page_source)
page_num = selector.css("#dnn_ctr59825_ArticleList__ctl0_plPageNum::text")

print(page_num)
# print(browser.page_source)

browser.quit()