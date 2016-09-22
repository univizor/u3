from feeder.spiders import FeederSpider
from scrapy import Request
from re import search, sub
from feeder.items import Source
import arrow
import math


class RUL(FeederSpider):
    name = "rul"
    base_url = 'https://repozitorij.uni-lj.si'
    domain = 'repozitorij.uni-lj.si'
    # allowed_domains = ['repozitorij.uni-lj.si', 'uni-lj.si', 'si']
    mode = 'refresh'

    @property
    def categories(self):
        return self.over_categories if self.over_categories else [
            'kat1=jezik&kat2=1060'
        ]

    def start_requests(self):
        return (Request("%s/Brskanje2.php?%s" % (self.base_url, category), meta={'isIndex': True}) for category in
                self.categories)

    def parse(self, response):
        if 'isIndex' in response.meta:
            return self.parse_index(response)

        if 'isRedirect' in response.meta:
            return self.parse_redirect(response)

        return self.parse_page(response)

    def parse_index(self, response):
        num_record = int(str(response.css('div.StZadetkov::text').extract()[0].split(' ')[0]))
        pages = math.ceil(num_record / 10.0) if not self.over_pages else self.over_pages
        return [Request(response.url + "&page=%d" % page) for page in range(1, pages)]

    def parse_page(self, response):
        urls = set([self.prepare_url(url) for url in response.css("a[href^='Dokument.php']").xpath("@href").extract()])
        return [Request(url, meta={'isRedirect': True}) for url in urls if not self.exists_by({'scraped_url': url})]

    def better_parse_page(self, response):
        urls = [search("Dokument.php\?id=\d+", p).group(0) for p in response
            .css("div.Besedilo p:last-child")
            .extract() if "datoteka" in p]

        urls = set([self.prepare_url(url) for url in urls])

        return [Request(url, meta={'isRedirect': True}) for url in urls if not self.exists_by({'scraped_url': url})]

    def parse_redirect(self, response):
        url = response.url

        if self.exists_by({'scraped_url': url}):
            return None

        return Source(
            domain=self.domain,
            scraped_at=arrow.utcnow(),
            scraped_url=url,
            file_urls=[url]
        )

    def prepare_url(self, url):
        return ('' + self.base_url + '/' + url).split('&')[0]
