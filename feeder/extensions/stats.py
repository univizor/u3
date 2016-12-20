from scrapy import signals
from twisted.internet.task import LoopingCall
from feeder.settings import DOGSTATSD_ADDR, DOGSTATSD_PORT, PERSIST_STATS_INTERVAL
from datadog import statsd, DogStatsd


class DatadogStats(object):
    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(PERSIST_STATS_INTERVAL)
        crawler.signals.connect(obj.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(obj.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(obj.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(obj.spider_error, signal=signals.spider_error)

        crawler.signals.connect(obj.item_scraped, signal=signals.item_scraped)
        return obj

    def __init__(self, interval):
        self.items_scraped = 0
        self.interval = interval
        self.tasks = {}
        self.statsd = DogStatsd(
            host=DOGSTATSD_ADDR,
            port=DOGSTATSD_PORT,
            # max_buffer_size=1,
            # constant_tags=[]
        )

    def increment(self, metric, value=1, tags=None):
        self.statsd.increment(metric, value=1, tags=tags)

    def gauge(self, metric, value, tags=None):
        self.statsd.gauge(metric, value=value, tags=tags)

    def spider_opened(self, spider):
        task = self.tasks[spider.name] = LoopingCall(self.persist_stats, spider)
        task.start(self.interval)
        self.increment("u3.spider.spider_opened", tags=['spider:%s' % spider.name])

    def spider_idle(self, spider):
        self.increment("u3.spider.spider_idle", tags=['spider:%s' % spider.name])

    def spider_closed(self, spider):
        task = self.tasks.pop(spider.name)
        task.stop()
        self.increment("u3.spider.spider_closed", tags=['spider:%s' % spider.name])

    def spider_error(self, spider):
        self.increment("u3.spider.spider_error", tags=['spider:%s' % spider.name])

    def item_scraped(self, item, spider):
        self.items_scraped += 1
        self.increment("u3.spider.item_scraped", tags=['spider:%s' % spider.name])
        self.increment("u3.spider.items_scraped", tags=['spider:%s' % spider.name])

    def persist_stats(self, spider):
        tags = ['spider:%s' % spider.name]
        self.increment("u3.spider.persist_stats", tags=tags)
        data = spider.crawler.stats.get_stats()
        normal_data = {("u3.spider.%s" % k.replace("/", ".")): v for k, v in data.items() if isinstance(v, int)}
        for k, v in normal_data.items():
            if "count" in k:
                self.increment(k, v, tags=tags)
            else:
                self.gauge(k, v, tags=tags)
