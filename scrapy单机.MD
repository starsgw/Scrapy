1.第一次安装scrapy会出现报错，需要安装Twisted后安装scrapy
安装Twisted 可在cmd中用下载命令：python -m pip install Twisted，它是用Python实现的基于事件驱动的网络引擎框架。下载地址： http://twistedmatrix.com/trac/wiki/Downloads

2.在某个文件夹下创建scrapy项目：(cd进入到那个文件夹)
使用指令：scrapy  startproject  scrapy_test(项目名)

3.创建spider
进入到项目文件夹:cd  scrapy_test
创建spider: scrapy  genspider  quotes  quotes.toscrape.com  (生成quotes这个spider)

3.1在items.py中定义item
from ..items import WenkuxiazaiItem

import scrapy

class WenkuxiazaiItem(scrapy.Item): #用于定义爬取的数据结构
    # define the fields for your item here like:
    # name = scrapy.Field()
    text=scrapy.Field()



4.在parse中解析需要的数据,并使用item（item可以理解为一个字典）
class QuotesSpider(scrapy.Spider):
    name = 'quotes'#spider的名称/用于区分不同的spider
    allowed_domains = ['quotes.toscrape.com']#允许爬取的网站域名,如果初始或者后续的请求链接不是这个域名下的，则请求链接会被过滤掉
    start_urls = ['http://quotes.toscrape.com/']#包含啦spider在启动时爬取的url列表，初始请求由它

def parse(self, response):#spider的一个方法/默认情况下，被调用时start_urls里面的链接请求构成的请求完成下载执行后，返回的响应就会作为唯一的参数传递给这个函数。/该方法负责解析返回的响应，提取数据或者进一步生成要处理的请求
text_list=response.xpath("//div[@class='quote']/span[@class='text']/font/text()")
    for text in text_list:
        item=ScrapyTestItem()
        item['text']=text
        yield item

5.后续Request操作
（解析出能获取下一页的链接，并构造下一个请求）
def parse(self, response):#spider的一个方法/默认情况下，被调用时start_urls里面的链接请求构成的请求完成下载执行后，返回的响应就会作为唯一的参数传递给这个函数。/该方法负责解析返回的响应，提取数据或者进一步生成要处理的请求
    text_list=response.xpath("//div[@class='quote']/span[@class='text']/font/text()")
    for text in text_list:
        item=ScrapyTestItem()
        item['text']=text
        yield item

    next=response.xpath("//nav/ul/li/a/@href")#下一页的链接
If next:
        url=response.urljoin(next)
        yield scrapy.Request(url=url,callback=self.parse)


6.运行(运行会出现报错ModuleNotFoundError: No module named 'win32api'，因为Python没有自带访问windows系统API的库的，需要下载第三方库。库的名称叫pywin32)
Scrapy  crawl  quotes

7.重写初次请求（从start_urls中请求）
def start_requests(self):
    for url in self.start_urls:
           print("2",self.start_urls)
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

8.设置代理：在middlewares.py文件中加入代理（在items.py同级新建get_ip文件，里面获取ip）
from .get_dtip import get_ip,get_ip2

class ProxyMiddleware(object):
    def process_request(self,request,spider):
        try:
            ip = get_ip()
            print("ip1",random.choice(ip))
            request.meta['proxy'] = random.choice(ip)
        except:
            ip2 = get_ip2()
            print('ip2',random.choice(ip2))
            request.meta['proxy'] = random.choice(ip2)

8.1然后在Settings.py中设置：
DOWNLOADER_MIDDLEWARES = {
   # 'Wenkuxiazai.middlewares.WenkuxiazaiDownloaderMiddleware': 543,
    'Wenkuxiazai.middlewares.ProxyMiddleware': 544,
}

9.设置请求头：（在spider文件夹中的项目中）
# // 添加的请求头(方法一)
custom_settings = {
                      # 'LOG_LEVEL': 'DEBUG',
                      # 'LOG_FILE': '5688_log_%s.txt' % time.time(),
"DEFAULT_REQUEST_HEADERS": {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Connection": "keep-alive",
    "Host": "www.wenkuxiazai.com",
    "Referer": "https://www.wenkuxiazai.com/",
    'User-Agent':random.choice(User_Agent),
}
}


10.管道设置：（将数据存入Mongodb）
class WenkuxiazaiPipeline(object):
    def process_item(self, item, spider):
        return item

import pymongo

class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri=mongo_uri
        self.mongo_db=mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri= crawler.settings.get('MONGO_URI'),
            mongo_db= crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        # name = item.__class__.__name__
        try:
            name="wenkuxiazaiwang_data"
            self.db[name].insert(dict(item))
            print("插入成功")
            return item
        except:
            print("重复数据")

    def close_spider(self,spider):
        self.client.close()

10.1然后在Settings.py中设置：
ITEM_PIPELINES = {
   # 'Wenkuxiazai.pipelines.WenkuxiazaiPipeline': 300,
    'Wenkuxiazai.pipelines.MongoPipeline':400,
}

MONGO_URI = "192.168.8.211"#在全局配置mongodb连接需要的地址和数据库名称
MONGO_DB = "Runoob"

11.启动：在items.py文件的同级目录新建main.py文件，可直接运行scrapy项目（和在指令窗口输入指令一样）
from scrapy import cmdline

cmdline.execute(("scrapy crawl wenku_data".split()))#运行
# cmdline.execute(("scrapy crawl quotes -o quotes.json".split()))#保存为想要的格式到本地
