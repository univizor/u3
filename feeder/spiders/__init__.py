# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from feeder.models import *
from sqlalchemy.orm import sessionmaker


class FeederSpider(scrapy.Spider):
    mode = 'refresh'
    over_pages = None
    over_categories = None

    def __init__(self, mode='refresh', pages=None, categories=None, *args, **kwargs):
        super(FeederSpider, self).__init__(*args, **kwargs)
        self.mode = mode

        engine = db_connect()
        self.Session = sessionmaker(bind=engine)
        self.repository = self.Session()

        if pages is not None:
            self.over_pages = int('' + pages)

        if categories is not None:
            self.over_categories = ('' + categories).split(',')

    def __del__(self):
        if self.repository:
            self.repository.close()

    def exists_by(self, properties):
        query = self.repository.query(DBSource) \
            .filter(DBSource.scraped_url == properties['scraped_url'])
        return self.repository.query(query.exists()) \
            .scalar()
