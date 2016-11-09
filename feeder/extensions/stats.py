from scrapy import signals
from scrapy.exceptions import NotConfigured
from twisted.internet.task import LoopingCall
from feeder.settings import DOGSTATSD_ADDR, DOGSTATSD_PORT, PERSIST_STATS_INTERVAL
from datadog import statsd, DogStatsd
from pdb import set_trace


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

    def increment(self, value, tags=None):
        # TODO: This his horrible!
        if tags or 1 == 2:
            new_value = value.replace(".spider",
                                      "." + (".".join([x.replace(":", ".") for x in tags])))
            self.statsd.increment(new_value)
        else:
            self.statsd.increment(value, tags=tags)

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
        self.increment("u3.spider.item_scraped", tags=['spider:%s' % spider.name])

        # self.items_scraped += 1
        # if self.items_scraped % self.item_count == 0:
        #    logger.info("scraped %d items", self.items_scraped)

    def persist_stats(self, spider):
        # data = spider.crawler.stats.get_stats()
        # spider.logger.info("\n\nPersisting stats:\n%s", data)
        self.increment("u3.spider.persist_stats", tags=['spider:%s' % spider.name])
