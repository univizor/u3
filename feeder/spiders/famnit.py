from feeder.spiders import FeederSpider
from scrapy import Request
from feeder.items import Source
import arrow
import json


class FAMMIT(FeederSpider):
    name = "fammit"
    domain = "famnit.upr.si"
    base_url = 'http://www.famnit.upr.si'
    mode = 'refresh'

    @property
    def categories(self):
        return self.over_categories if self.over_categories else range(2008, arrow.now().year + 1)

    def start_requests(self):
        return (Request("%s/sl/studij/zakljucna_dela/search:json" % self.base_url,
                        method="POST",
                        headers={
                            'Content-Type': 'application/json',
                            'Origin': 'http://www.famnit.upr.si',
                            'X-Requested-With': 'XMLHttpRequest'
                        },
                        body=json.dumps({
                            "search_string": str(category),
                            "search_opts": {"title": False, "year": True, "author": False, "mentor": False,
                                            "somentor": False, "keywords": False, "abstract": False, "smer": False,
                                            "text": False
                                            }
                        })) for category in self.categories)

    def parse(self, response):
        if "search" in response.url:
            return self.parse_index(response)

    def parse_index(self, response):
        list = [item["id"] for item in json.loads(response.body_as_unicode(), 'utf-8')["list"]]
        urls = set([self.prepare_url(id) for id in list])

        return [Source(
            domain=self.domain,
            scraped_at=arrow.utcnow(),
            scraped_url=url,
            file_urls=[url]
        ) for url in urls if not self.exists_by({'scraped_url': url})]

    def prepare_url(self, id):
        return self.base_url + "/sl/studij/zakljucna_dela/download/%s" % id
