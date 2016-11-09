from scrapy import signals
from twisted.internet.task import LoopingCall
from feeder.settings import DOGSTATSD_ADDR, DOGSTATSD_PORT, PERSIST_STATS_INTERVAL
from datadog import statsd, DogStatsd


class DatadogStats(object):
    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(PERSIST_STATS_INTERVAL)
        crawler.signals.connect(obj.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(obj.spider_closed, signal=signals.spider_closed)
        return obj

    def __init__(self, interval):
        self.interval = interval
        self.tasks = {}
        self.statsd = DogStatsd(
            host=DOGSTATSD_ADDR,
            port=DOGSTATSD_PORT,
            constant_tags=["crawler"]
        )

    def spider_opened(self, spider):
        task = self.tasks[spider.name] = LoopingCall(self.perist_stats, spider)
        task.start(self.interval)

    def spider_closed(self, spider):
        task = self.tasks.pop(spider.name)
        task.stop()

    def perist_stats(self, spider):
        data = spider.crawler.stats.get_stats()
        spider.logger.info("\n\nPersisting stats:\n%s", data)
        self.statsd.increment("stats_collection")
