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
DB_HOST = "haystack.cety7wul5z9k.us-west-2.rds.amazonaws.com"
DB_USER = "deployer"
DB_PASSWD = "p0877e546c0539179b1fb234649e2aba6691a28b53815b7710a93d65cc21c2059"
DB_NAME = "haystack3_production"

#"""
PROXIES = [
    {"host": "3000.usa.rotating.proxyrack.net:3000"},
    {"host": "3001.usa.rotating.proxyrack.net:3001"},
    {"host": "3002.usa.rotating.proxyrack.net:3002"},
    {"host": "3003.usa.rotating.proxyrack.net:3003"},
    {"host": "3004.usa.rotating.proxyrack.net:3004"},
    {"host": "3005.usa.rotating.proxyrack.net:3005"},
    {"host": "3006.usa.rotating.proxyrack.net:3006"},
    {"host": "3007.usa.rotating.proxyrack.net:3007"},
    {"host": "3008.usa.rotating.proxyrack.net:3008"},
    {"host": "3009.usa.rotating.proxyrack.net:3009"},
    {"host": "3010.usa.rotating.proxyrack.net:3010"},
    {"host": "3011.usa.rotating.proxyrack.net:3011"},
    {"host": "3012.usa.rotating.proxyrack.net:3012"},
    {"host": "3013.usa.rotating.proxyrack.net:3013"},
    {"host": "3014.usa.rotating.proxyrack.net:3014"},
    {"host": "3015.usa.rotating.proxyrack.net:3015"},
    {"host": "3016.usa.rotating.proxyrack.net:3016"},
    {"host": "3017.usa.rotating.proxyrack.net:3017"},
    {"host": "3018.usa.rotating.proxyrack.net:3018"},
    {"host": "3019.usa.rotating.proxyrack.net:3019"},
    {"host": "3020.usa.rotating.proxyrack.net:3020"},
    {"host": "3021.usa.rotating.proxyrack.net:3021"},
    {"host": "3022.usa.rotating.proxyrack.net:3022"},
    {"host": "3023.usa.rotating.proxyrack.net:3023"},
    {"host": "3024.usa.rotating.proxyrack.net:3024"},
    {"host": "3025.usa.rotating.proxyrack.net:3025"},
    {"host": "3026.usa.rotating.proxyrack.net:3026"},
    {"host": "3027.usa.rotating.proxyrack.net:3027"},
    {"host": "3028.usa.rotating.proxyrack.net:3028"},
    {"host": "3029.usa.rotating.proxyrack.net:3029"},
    {"host": "3030.usa.rotating.proxyrack.net:3030"},
    {"host": "3031.usa.rotating.proxyrack.net:3031"},
    {"host": "3032.usa.rotating.proxyrack.net:3032"},
    {"host": "3033.usa.rotating.proxyrack.net:3033"},
    {"host": "3034.usa.rotating.proxyrack.net:3034"},
    {"host": "3035.usa.rotating.proxyrack.net:3035"},
    {"host": "3036.usa.rotating.proxyrack.net:3036"},
    {"host": "3037.usa.rotating.proxyrack.net:3037"},
    {"host": "3038.usa.rotating.proxyrack.net:3038"},
    {"host": "3039.usa.rotating.proxyrack.net:3039"},
    {"host": "3040.usa.rotating.proxyrack.net:3040"},
    {"host": "3041.usa.rotating.proxyrack.net:3041"},
    {"host": "3042.usa.rotating.proxyrack.net:3042"},
    {"host": "3043.usa.rotating.proxyrack.net:3043"},
    {"host": "3044.usa.rotating.proxyrack.net:3044"},
    {"host": "3045.usa.rotating.proxyrack.net:3045"},
    {"host": "3046.usa.rotating.proxyrack.net:3046"},
    {"host": "3047.usa.rotating.proxyrack.net:3047"},
    {"host": "3048.usa.rotating.proxyrack.net:3048"},
    {"host": "3049.usa.rotating.proxyrack.net:3049"},
    {"host": "3050.usa.rotating.proxyrack.net:3050"},
    {"host": "3051.usa.rotating.proxyrack.net:3051"},
    {"host": "3052.usa.rotating.proxyrack.net:3052"},
    {"host": "3053.usa.rotating.proxyrack.net:3053"},
    {"host": "3054.usa.rotating.proxyrack.net:3054"},
    {"host": "3055.usa.rotating.proxyrack.net:3055"},
    {"host": "3056.usa.rotating.proxyrack.net:3056"},
    {"host": "3057.usa.rotating.proxyrack.net:3057"},
    {"host": "3058.usa.rotating.proxyrack.net:3058"},
    {"host": "3059.usa.rotating.proxyrack.net:3059"},
    {"host": "3060.usa.rotating.proxyrack.net:3060"},
    {"host": "3061.usa.rotating.proxyrack.net:3061"},
    {"host": "3062.usa.rotating.proxyrack.net:3062"},
    {"host": "3063.usa.rotating.proxyrack.net:3063"},
    {"host": "3064.usa.rotating.proxyrack.net:3064"},
    {"host": "3065.usa.rotating.proxyrack.net:3065"},
    {"host": "3066.usa.rotating.proxyrack.net:3066"},
    {"host": "3067.usa.rotating.proxyrack.net:3067"},
    {"host": "3068.usa.rotating.proxyrack.net:3068"},
    {"host": "3069.usa.rotating.proxyrack.net:3069"},
    {"host": "3070.usa.rotating.proxyrack.net:3070"},
    {"host": "3071.usa.rotating.proxyrack.net:3071"},
    {"host": "3072.usa.rotating.proxyrack.net:3072"},
    {"host": "3073.usa.rotating.proxyrack.net:3073"},
    {"host": "3074.usa.rotating.proxyrack.net:3074"},
    {"host": "3075.usa.rotating.proxyrack.net:3075"},
    {"host": "3076.usa.rotating.proxyrack.net:3076"},
    {"host": "3077.usa.rotating.proxyrack.net:3077"},
    {"host": "3078.usa.rotating.proxyrack.net:3078"},
    {"host": "3079.usa.rotating.proxyrack.net:3079"},
    {"host": "3080.usa.rotating.proxyrack.net:3080"},
    {"host": "3081.usa.rotating.proxyrack.net:3081"},
    {"host": "3082.usa.rotating.proxyrack.net:3082"},
    {"host": "3083.usa.rotating.proxyrack.net:3083"},
    {"host": "3084.usa.rotating.proxyrack.net:3084"},
    {"host": "3085.usa.rotating.proxyrack.net:3085"},
    {"host": "3086.usa.rotating.proxyrack.net:3086"},
    {"host": "3087.usa.rotating.proxyrack.net:3087"},
    {"host": "3088.usa.rotating.proxyrack.net:3088"},
    {"host": "3089.usa.rotating.proxyrack.net:3089"},
    {"host": "3090.usa.rotating.proxyrack.net:3090"},
    {"host": "3091.usa.rotating.proxyrack.net:3091"},
    {"host": "3092.usa.rotating.proxyrack.net:3092"},
    {"host": "3093.usa.rotating.proxyrack.net:3093"},
    {"host": "3094.usa.rotating.proxyrack.net:3094"},
    {"host": "3095.usa.rotating.proxyrack.net:3095"},
    {"host": "3096.usa.rotating.proxyrack.net:3096"},
    {"host": "3097.usa.rotating.proxyrack.net:3097"},
    {"host": "3098.usa.rotating.proxyrack.net:3098"},
    {"host": "3099.usa.rotating.proxyrack.net:3099"},
    {"host": "3100.usa.rotating.proxyrack.net:3100"},
    {"host": "3101.usa.rotating.proxyrack.net:3101"},
    {"host": "3102.usa.rotating.proxyrack.net:3102"},
    {"host": "3103.usa.rotating.proxyrack.net:3103"},
    {"host": "3104.usa.rotating.proxyrack.net:3104"},
    {"host": "3105.usa.rotating.proxyrack.net:3105"},
    {"host": "3106.usa.rotating.proxyrack.net:3106"},
    {"host": "3107.usa.rotating.proxyrack.net:3107"},
    {"host": "3108.usa.rotating.proxyrack.net:3108"},
    {"host": "3109.usa.rotating.proxyrack.net:3109"},
    {"host": "3110.usa.rotating.proxyrack.net:3110"},
    {"host": "3111.usa.rotating.proxyrack.net:3111"},
    {"host": "3112.usa.rotating.proxyrack.net:3112"},
    {"host": "3113.usa.rotating.proxyrack.net:3113"},
    {"host": "3114.usa.rotating.proxyrack.net:3114"},
    {"host": "3115.usa.rotating.proxyrack.net:3115"},
    {"host": "3116.usa.rotating.proxyrack.net:3116"},
    {"host": "3117.usa.rotating.proxyrack.net:3117"},
    {"host": "3118.usa.rotating.proxyrack.net:3118"},
    {"host": "3119.usa.rotating.proxyrack.net:3119"},
    {"host": "3120.usa.rotating.proxyrack.net:3120"},
    {"host": "3121.usa.rotating.proxyrack.net:3121"},
    {"host": "3122.usa.rotating.proxyrack.net:3122"},
    {"host": "3123.usa.rotating.proxyrack.net:3123"},
    {"host": "3124.usa.rotating.proxyrack.net:3124"},
    {"host": "3125.usa.rotating.proxyrack.net:3125"},
    {"host": "3126.usa.rotating.proxyrack.net:3126"},
    {"host": "3127.usa.rotating.proxyrack.net:3127"},
    {"host": "3128.usa.rotating.proxyrack.net:3128"},
    {"host": "3129.usa.rotating.proxyrack.net:3129"},
    {"host": "3130.usa.rotating.proxyrack.net:3130"},
    {"host": "3131.usa.rotating.proxyrack.net:3131"},
    {"host": "3132.usa.rotating.proxyrack.net:3132"},
    {"host": "3133.usa.rotating.proxyrack.net:3133"},
    {"host": "3134.usa.rotating.proxyrack.net:3134"},
    {"host": "3135.usa.rotating.proxyrack.net:3135"},
    {"host": "3136.usa.rotating.proxyrack.net:3136"},
    {"host": "3137.usa.rotating.proxyrack.net:3137"},
    {"host": "3138.usa.rotating.proxyrack.net:3138"},
    {"host": "3139.usa.rotating.proxyrack.net:3139"},
    {"host": "3140.usa.rotating.proxyrack.net:3140"},
    {"host": "3141.usa.rotating.proxyrack.net:3141"},
    {"host": "3142.usa.rotating.proxyrack.net:3142"},
    {"host": "3143.usa.rotating.proxyrack.net:3143"},
    {"host": "3144.usa.rotating.proxyrack.net:3144"},
    {"host": "3145.usa.rotating.proxyrack.net:3145"},
    {"host": "3146.usa.rotating.proxyrack.net:3146"},
    {"host": "3147.usa.rotating.proxyrack.net:3147"},
    {"host": "3148.usa.rotating.proxyrack.net:3148"},
    {"host": "3149.usa.rotating.proxyrack.net:3149"},
    {"host": "3150.usa.rotating.proxyrack.net:3150"},
    {"host": "3151.usa.rotating.proxyrack.net:3151"},
    {"host": "3152.usa.rotating.proxyrack.net:3152"},
    {"host": "3153.usa.rotating.proxyrack.net:3153"},
    {"host": "3154.usa.rotating.proxyrack.net:3154"},
    {"host": "3155.usa.rotating.proxyrack.net:3155"},
    {"host": "3156.usa.rotating.proxyrack.net:3156"},
    {"host": "3157.usa.rotating.proxyrack.net:3157"},
    {"host": "3158.usa.rotating.proxyrack.net:3158"},
    {"host": "3159.usa.rotating.proxyrack.net:3159"},
    {"host": "3160.usa.rotating.proxyrack.net:3160"},
    {"host": "3161.usa.rotating.proxyrack.net:3161"},
    {"host": "3162.usa.rotating.proxyrack.net:3162"},
    {"host": "3163.usa.rotating.proxyrack.net:3163"},
    {"host": "3164.usa.rotating.proxyrack.net:3164"},
    {"host": "3165.usa.rotating.proxyrack.net:3165"},
    {"host": "3166.usa.rotating.proxyrack.net:3166"},
    {"host": "3167.usa.rotating.proxyrack.net:3167"},
    {"host": "3168.usa.rotating.proxyrack.net:3168"},
    {"host": "3169.usa.rotating.proxyrack.net:3169"},
    {"host": "3170.usa.rotating.proxyrack.net:3170"},
    {"host": "3171.usa.rotating.proxyrack.net:3171"},
    {"host": "3172.usa.rotating.proxyrack.net:3172"},
    {"host": "3173.usa.rotating.proxyrack.net:3173"},
    {"host": "3174.usa.rotating.proxyrack.net:3174"},
    {"host": "3175.usa.rotating.proxyrack.net:3175"},
    {"host": "3176.usa.rotating.proxyrack.net:3176"},
    {"host": "3177.usa.rotating.proxyrack.net:3177"},
    {"host": "3178.usa.rotating.proxyrack.net:3178"},
    {"host": "3179.usa.rotating.proxyrack.net:3179"},
    {"host": "3180.usa.rotating.proxyrack.net:3180"},
    {"host": "3181.usa.rotating.proxyrack.net:3181"},
    {"host": "3182.usa.rotating.proxyrack.net:3182"},
    {"host": "3183.usa.rotating.proxyrack.net:3183"},
    {"host": "3184.usa.rotating.proxyrack.net:3184"},
    {"host": "3185.usa.rotating.proxyrack.net:3185"},
    {"host": "3186.usa.rotating.proxyrack.net:3186"},
    {"host": "3187.usa.rotating.proxyrack.net:3187"},
    {"host": "3188.usa.rotating.proxyrack.net:3188"},
    {"host": "3189.usa.rotating.proxyrack.net:3189"},
    {"host": "3190.usa.rotating.proxyrack.net:3190"},
    {"host": "3191.usa.rotating.proxyrack.net:3191"},
    {"host": "3192.usa.rotating.proxyrack.net:3192"},
    {"host": "3193.usa.rotating.proxyrack.net:3193"},
    {"host": "3194.usa.rotating.proxyrack.net:3194"},
    {"host": "3195.usa.rotating.proxyrack.net:3195"},
    {"host": "3196.usa.rotating.proxyrack.net:3196"},
    {"host": "3197.usa.rotating.proxyrack.net:3197"},
    {"host": "3198.usa.rotating.proxyrack.net:3198"},
    {"host": "3199.usa.rotating.proxyrack.net:3199"},
    {"host": "3200.usa.rotating.proxyrack.net:3200"},
    {"host": "3201.usa.rotating.proxyrack.net:3201"},
    {"host": "3202.usa.rotating.proxyrack.net:3202"},
    {"host": "3203.usa.rotating.proxyrack.net:3203"},
    {"host": "3204.usa.rotating.proxyrack.net:3204"},
    {"host": "3205.usa.rotating.proxyrack.net:3205"},
    {"host": "3206.usa.rotating.proxyrack.net:3206"},
    {"host": "3207.usa.rotating.proxyrack.net:3207"},
    {"host": "3208.usa.rotating.proxyrack.net:3208"},
    {"host": "3209.usa.rotating.proxyrack.net:3209"},
    {"host": "3210.usa.rotating.proxyrack.net:3210"},
    {"host": "3211.usa.rotating.proxyrack.net:3211"},
    {"host": "3212.usa.rotating.proxyrack.net:3212"},
    {"host": "3213.usa.rotating.proxyrack.net:3213"},
    {"host": "3214.usa.rotating.proxyrack.net:3214"},
    {"host": "3215.usa.rotating.proxyrack.net:3215"},
    {"host": "3216.usa.rotating.proxyrack.net:3216"},
    {"host": "3217.usa.rotating.proxyrack.net:3217"},
    {"host": "3218.usa.rotating.proxyrack.net:3218"},
    {"host": "3219.usa.rotating.proxyrack.net:3219"},
    {"host": "3220.usa.rotating.proxyrack.net:3220"},
    {"host": "3221.usa.rotating.proxyrack.net:3221"},
    {"host": "3222.usa.rotating.proxyrack.net:3222"},
    {"host": "3223.usa.rotating.proxyrack.net:3223"},
    {"host": "3224.usa.rotating.proxyrack.net:3224"},
    {"host": "3225.usa.rotating.proxyrack.net:3225"},
    {"host": "3226.usa.rotating.proxyrack.net:3226"},
    {"host": "3227.usa.rotating.proxyrack.net:3227"},
    {"host": "3228.usa.rotating.proxyrack.net:3228"},
    {"host": "3229.usa.rotating.proxyrack.net:3229"},
    {"host": "3230.usa.rotating.proxyrack.net:3230"},
    {"host": "3231.usa.rotating.proxyrack.net:3231"},
    {"host": "3232.usa.rotating.proxyrack.net:3232"},
    {"host": "3233.usa.rotating.proxyrack.net:3233"},
    {"host": "3234.usa.rotating.proxyrack.net:3234"},
    {"host": "3235.usa.rotating.proxyrack.net:3235"},
    {"host": "3236.usa.rotating.proxyrack.net:3236"},
    {"host": "3237.usa.rotating.proxyrack.net:3237"},
    {"host": "3238.usa.rotating.proxyrack.net:3238"},
    {"host": "3239.usa.rotating.proxyrack.net:3239"},
    {"host": "3240.usa.rotating.proxyrack.net:3240"},
    {"host": "3241.usa.rotating.proxyrack.net:3241"},
    {"host": "3242.usa.rotating.proxyrack.net:3242"},
    {"host": "3243.usa.rotating.proxyrack.net:3243"},
    {"host": "3244.usa.rotating.proxyrack.net:3244"},
    {"host": "3245.usa.rotating.proxyrack.net:3245"},
    {"host": "3246.usa.rotating.proxyrack.net:3246"},
    {"host": "3247.usa.rotating.proxyrack.net:3247"},
    {"host": "3248.usa.rotating.proxyrack.net:3248"},
    {"host": "3249.usa.rotating.proxyrack.net:3249"},
    {"host": "3250.usa.rotating.proxyrack.net:3250"}
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
"""
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

