from feeder.spiders import FeederSpider
from scrapy import Request
from feeder.items import Source
import arrow


class UNG(FeederSpider):
    name = "ung"
    domain = "sabotin.ung.si"
    base_url = 'http://sabotin.ung.si'
    mode = 'refresh'

    @property
    def categories(self):
        return self.over_categories if self.over_categories else [
            'diplome', 'doktorati', 'magisterij'
        ]

    def start_requests(self):
        return (Request("%s/~library/%s" % (self.base_url, category)) for category in self.categories)

    def parse(self, response):
        if "Index" in response.body_as_unicode():
            return self.parse_index(response)

    def parse_index(self, response):
        links = response.css('a').xpath("@href").extract()[5:]
        urls = [self.request_or_source("%s%s" % (response.url, link)) for link in links]
        return [url for url in urls if not url is None]

    def request_or_source(self, url):
        if url.endswith('.pdf'):
            if self.exists_by({'scraped_url': url}):
                return None

            return Source(
                domain=self.domain,
                scraped_at=arrow.utcnow(),
                scraped_url=url,
                file_urls=[url]
            )
        elif url.endswith('/'):
            return Request(url)
        else:
            return None
