# SHUMES_Spider
* scrapy-redis是分布式的一个开源插件 目前还在学习中
没有实际操作
* SHUSpider中有未完成的spider 请小心使用
* 数据库的部署在setting中 需要根据自己的使用再次修改
* pipeline中写的是异步的数据库导入
* main中可以直接调试或者运行需要使用的spider
* utils中有login的代码：
    * 成就系统（验证码这部分没写上去 比较麻烦 如果是手动写验证码 就很难以后部署scrapy）
    * 熟知网的json格式获取 由于比较简单就没有写成spider 不过后面要部署scrapy就需要修改成spider
##### 比较完善的Spider
* librarynews 图书馆整站爬取
* SHUnews 需要修改其中的tag才能爬取相对应的系列
* enrolnews本科招生网中的通知公告，还有一个系列是工作动态 目前只有一条有效
    * 需要修改才能爬取另外一个系列
##### 正在完善的spider
* SHUnews 需要修改其中的tag才能爬取相对应的系列 
    * 正在调整代码 使其可以直接获取全站新闻
* jwc 教务处正在完善中 （只写了一点点）
* workSHU就业信息服务网 这个网站格式不太一样
##### 被放弃的spider
* 新闻网中的媒体关注 直接跳转到外网 爬取需要体力 已放弃
* 成就系统szSHU 大部分转接给熟知网了
