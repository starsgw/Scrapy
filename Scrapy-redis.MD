关于scrapy-redis的地址：https://github.com/rmax/scrapy-redis
搭建分布式爬虫
参考官网地址：https://scrapy-redis.readthedocs.io/en/stable/
前提是要安装scrapy_redis模块：pip install scrapy_redis

一．开启服务器的redis服务
  1、看书上敲出单机的scrapy代码     ---  C:\Users\Administrator\tutorial
2、部署linux  redis服务器，保证windows客户端能连接上
	（1）下载：
 		wget http://download.redis.io/releases/redis-4.0.6.tar.gz
		tar xzf redis-4.0.6.tar.gz
		cd redis-4.0.6
		make
   		make install
	  (2)   启动服务
		./src/redis-server
	（3）修改配置文件
		vim redis.conf
		注释bind127.0.0.1
		设置密码: 打开注释 requirepass 123456 (123456)为密码
		daemonize no   改为 yes
		protected-mode yes 改为no
	（4）运用刚刚保存的配置并启动redis：
		cd src
		./redis-server ../redis.conf
	 （5）windows窗口 cmd ,输入telnet 192.168.1.17 6379连接测试（需要首先控制面板 “打开或关闭Windows功能”中添加“telnet客户端”）    如果出现黑屏连接成功
	（6）用可视化工具连接

3、设置开机启动(非必要)
systemctl enable redis.service
4、设置redis密码(非必要)
打开文件/etc/redis.conf，找到其中的# requirepass foobared，去掉前面的#，并把foobared改成你的密码


二.修改该settings中的配置信息：
SCHEDULER = "scrapy_redis.scheduler.Scheduler"#替换scrapy调度器
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"#添加去重的class
# REDIS_URL = 'redis://[:123456]@196.168.8.243:6379'
REDIS_HOST = '192.168.8.243'
REDIS_PARAMS = {
            'password': '123456',
            'db':1
        }
REDIS_PORT = 6379
SCHEDULER_PERSIST = True#调度状态持久化，不清理redis缓存，允许暂停/启动爬虫
SCHEDULER_FLUSH_ON_START=False #设置重启爬虫时是否清空爬取队列,这样每次重启爬虫都会清空指纹和请求队列,一般设置为False

三．修改spider文件夹中的项目文件
将下面的：
class WenkuDataSpider(scrapy.Spider):                  
    name = 'wenku_data'
    allowed_domains = ['www.wenkuxiazai.com']
    index_url = 'https://www.wenkuxiazai.com/search/'
    page=0
    keyword = get_keyword()
    keyword = ""
    url = get_url_data(index_url,keyword,page)
    start_urls = [url]
改为：
from scrapy_redis.spiders import RedisSpider

class WenkuDataSpider(RedisSpider):               #修改啦继承类
    name = 'wenku_data'
    # allowed_domains = ['www.wenkuxiazai.com']      #屏蔽
    index_url = 'https://www.wenkuxiazai.com/search/'
    page=0
    # keyword = get_keyword()            
    keyword = ""
    # url = get_url_data(index_url,keyword,page)         
    # start_urls = [url]                              #屏蔽
    redis_key = 'wenkuxiazai:start_urls'              #会从redis中的wenkuxiazai:start_urls这个键取值



