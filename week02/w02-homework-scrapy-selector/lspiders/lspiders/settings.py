# Scrapy settings for lspiders project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lspiders'

SPIDER_MODULES = ['lspiders.spiders']
NEWSPIDER_MODULE = 'lspiders.spiders'

# 它原来直接把网页都pia出来...可能有用吧，真挺乱的，不知道python的日志框架怎么用，个别记录器应该能关闭吧
LOG_LEVEL='INFO'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'lspiders (+https://maoyan.com)'
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)
USER_AGENT = '{ua.random}'

# 以上，其实没搞明白，最终maoyan的那个遇到校验我就老老实实进去拖一下滚动条...然后接着调

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'lspiders.middlewares.LspidersSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'lspiders.middlewares.LspidersDownloaderMiddleware': 543,
   # 这里留着这个是为了调异常的，打开就走代理么，这纯听老师教的，没有任何延展部分
   'lspiders.middlewares.RandomHttpProxyMiddleware': 400,
}

# 上面的一行和底下的两行属于照抄自课程代码，底下这个从https://github.com/clarketm/proxy-list/blob/master/proxy-list-raw.txt，copy了几个，可能作业本意不是这个意思吧

HTTP_PROXY_LIST = [
     #'http://101.37.118.54:8888',
     # 'http://196.27.119.131:80',
     'http://200.215.171.238:8080',
]
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'lspiders.pipelines.LspidersPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
