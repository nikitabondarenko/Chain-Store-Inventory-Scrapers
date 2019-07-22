# -*- coding: utf-8 -*-

# Scrapy settings for products project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'products'

SPIDER_MODULES = ['products.spiders']
NEWSPIDER_MODULE = 'products.spiders'


# database configuration
DB_HOST = "127.0.0.1"
DB_USER = "postgres_user"
DB_PASSWD = "postgres_pass"
DB_NAME = "products"


#"""
PROXIES = [
    {"host": "https://us-ny.proxymesh.com:31280"},
    {"host": "https://us-il.proxymesh.com:31280"},
    {"host": "https://us-dc.proxymesh.com:31280"},
    {"host": "https://us-ca.proxymesh.com:31280"},
    {"host": "https://us-fl.proxymesh.com:31280"},
    {"host": "https://open.proxymesh.com:31280"}


#    {"host": "https://us.proxymesh.com:31280"},
]
"""

PROXIES = [
    {"host": "http://173.234.59.132:3128"},
    {"host": "http://170.130.67.40:3128"},
    {"host": "http://89.32.68.189:3128"},
    {"host": "http://173.234.194.100:3128"},
    {"host": "http://192.161.160.182:3128"},
    {"host": "http://89.32.71.182:3128"},
    {"host": "http://192.161.160.53:3128"},
    {"host": "http://170.130.67.21:3128"},
    {"host": "http://192.161.160.140:3128"},
    {"host": "http://173.234.194.136:3128"},
    {"host": "http://89.32.68.39:3128"},
    {"host": "http://173.234.59.247:3128"},
    {"host": "http://89.32.71.209:3128"},
    {"host": "http://192.161.160.233:3128"},
    {"host": "http://170.130.67.247:3128"},
    {"host": "http://173.234.194.226:3128"},
    {"host": "http://173.234.59.168:3128"},
    {"host": "http://89.32.68.160:3128"},
    {"host": "http://173.234.194.64:3128"},
    {"host": "http://89.32.71.91:3128"},
    {"host": "http://89.32.68.155:3128"},
    {"host": "http://89.32.68.10:3128"},
    {"host": "http://170.130.67.138:3128"},
    {"host": "http://89.32.71.111:3128"},
    {"host": "http://173.234.59.175:3128"},
    {"host": "https://us-il.proxymesh.com:31280"},
    {"host": "https://us-dc.proxymesh.com:31280"},
    {"host": "https://us-ca.proxymesh.com:31280"},
    {"host": "https://us-wa.proxymesh.com:31280"},
    {"host": "https://open.proxymesh.com:31280"},
    {"host": "https://us.proxymesh.com:31280"},
]
#"""
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64…) Gecko/20100101 Firefox/60.0"

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
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
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'products.middlewares.ProductsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'products.basic_middlewares.user_agent_middleware.RandomUserAgentMiddleware': 400,
    'products.basic_middlewares.proxy_middleware.ProxyMiddleware': 410,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'products.pipelines.PreProductsPipeline': 300,
    'products.pipelines.UnescapeNamePipeline': 310,
    'products.pipelines.TargetComPipeline': 400,
    'products.pipelines.StaplesComPipeline': 450,
    'products.pipelines.HomedepotComPipeline': 500,
    'products.pipelines.BedbathandbeyondComPipeline': 550,
    'products.pipelines.BarnesandnobleComPipeline': 600,
    'products.pipelines.PostProductsPipeline': 1000,
    'products.pipelines.PostgreSqlPipeline': 1100,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


import os
import logging
import datetime


#LOG_ENABLED = False
#LOG_LEVEL = "WARNING"
LOG_LEVEL = "DEBUG"
LOG_FILE = os.path.join('logs', datetime.datetime.now().strftime('%Y-%m-%d-%H-%M') + '.log')
#LOG_FILE = 'logs/' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M') + '.log'

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

