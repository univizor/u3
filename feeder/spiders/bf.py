from feeder.spiders import FeederSpider
from urllib.parse import urlencode

from scrapy import Request
from scrapy.utils.response import open_in_browser, body_or_str
from re import search, sub
from feeder.utils import html2text
from feeder.items import Source
import arrow
from re import sub
from json import loads, load
from pprint import pprint
from pdb import set_trace


class BF(FeederSpider):
    name = "bf"
    base_url = 'http://www.digitalna-knjiznica.bf.uni-lj.si'
    allowed_domains = ['*.bf.uni-lj.si']
    mode = 'refresh'

    @property
    def categories(self):
        return self.over_categories if self.over_categories else [
            'biologija', 'gozdarstvo', 'agronomija', 'zootehnika',
            'krajinska-arhitektura', 'lesarstvo', 'mikrobiologija',
            'zivilstvo', 'biotehnologija'
        ]

    def start_requests(self):
        return (Request("%s/%s.htm" % (self.base_url, category)) for category in self.categories)

    def parse(self, response):
        return self.parse_index(response)

    def parse_index(self, response):
        urls = set([self.prepare_url(url) for url in response
                   .css("a[href$=\".pdf\"]")
                   .xpath("@href")
                   .extract()])

        return [Source(
            domain='bf.uni-lj.si',
            scraped_at=arrow.utcnow(),
            scraped_url=url,
            file_urls=[url]
        ) for url in urls if not self.exists_by({'scraped_url': url})]

    def prepare_url(self, baseUrl):
        url = '' + baseUrl.strip()
        if not url.startswith('http://'):
            if not url.startswith('/'):
                url = self.base_url + "/" + url
            else:
                url = self.base_url + url

        return url
