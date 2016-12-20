# -*- coding: utf-8 -*-
from os import getenv, path, getcwd
from sqlalchemy.engine.url import URL

# Scrapy settings for startproject project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'feeder'
SPIDER_MODULES = ['feeder.spiders']
NEWSPIDER_MODULE = 'feeder.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'startproject (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = int(getenv("CONCURRENT_REQUESTS", "16"))

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = int(getenv("DOWNLOAD_DELAY", "3"))
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIES_DEBUG = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Stats (Datadog)
DOGSTATSD_ADDR = getenv("DOGSTATSD_PORT_8125_UDP_ADDR", getenv("GRAFANA_PORT_8125_UDP_ADDR", getenv("DOGSTATSD_ADDR")))
DOGSTATSD_PORT = int(
    getenv("DOGSTATSD_PORT_8125_UDP_PORT", getenv("GRAFANA_PORT_8125_UDP_PORT", getenv("DOGSTATSD_PORT", "0"))))
PERSIST_STATS_INTERVAL = int(getenv("PERSIST_STATS_INTERVAL", 10))

# Sentry exception logging
SENTRY_DSN = getenv("SENTRY_DSN")

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'startproject.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'startproject.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html

EXTENSIONS = {
    # 'scrapy.extensions.telnet.TelnetConsole': None,
    # 'feeder.extensions.stats.DatadogStats': 500
}

if DOGSTATSD_ADDR:
    EXTENSIONS['feeder.extensions.stats.DatadogStats'] = 500

if SENTRY_DSN:
    EXTENSIONS['scrapy_sentry.extensions.Errors'] = 10

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# from scrapy.contrib.pipeline.files import FilesPipeline

# from feeder.pipelines import FilesPipeline

ITEM_PIPELINES = {
    #    'startproject.pipelines.SomePipeline': 300,
    # 'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
    # 'feeder.pipelines.FilesPipeline': 1,
    'scrapy.pipelines.files.FilesPipeline': 1,
    # 'scrapy.pipelines.images.ImagesPipeline': 1,
    'feeder.pipelines.FeederPipeline': 2
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

TEMP_FILES_FOLDER = getenv('TEMP_FILES_FOLDER', path.join(getcwd(), "tmp/"))

FILES_STORE = getenv('FILES_STORE', './data/files')

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '7000',
    'username': 'postgres',
    'database': 'u3_dev'
    # 'port': '5432',
    # 'password': 'YOUR_PASSWORD',
}

DATABASE_URL = getenv('DATABASE_URL', URL(**DATABASE))
HASHING_ALGORITHM = getenv("HASHING_ALGORITHM", "sha256")  # 'sha1'
