from scrapy import Request
from feeder.items import Source
import arrow
from feeder.spiders.rul import RUL
import math
from scrapy.http import FormRequest
import os

# Add the temp dir settings - DKUM spider needs it
HOMEDIR = os.getenv('HOME')
TMPDIR = os.path.join(HOMEDIR, 'tmp/')

class DKUM(RUL):
    name = "dkum"
    base_url = 'https://dk.um.si'
    domain = "dk.um.si"
    # allowed_domains = ['dk.um.si', '*.um.si']
    mode = 'refresh'

    def parse(self, response):
        if 'isIndex' in response.meta:
            return self.parse_index(response)

        if 'isConsent' in response.meta:
            return self.parse_consent(response)

        return self.parse_page(response)

    def parse_index(self, response):
        num_record = int(str(response.css('div.Stat::text').extract()[0].split('/')[1]))
        pages = math.ceil(num_record / 10.0) if not self.over_pages else self.over_pages
        return [Request(response.url + "&page=%d" % page) for page in range(1, pages)]

    def parse_page(self, response):
        self.clear_tmp()
        urls = set([self.prepare_url(url) for url in response.css("a[href^='Dokument.php']").xpath("@href").extract()])
        return [Request(url, meta={'isConsent': True, 'cookiejar': url}) for url in urls if
                not self.exists_by({'scraped_url': url})]

    def parse_consent(self, response):
        key = response.css('input[name=key]').xpath("@value").extract()[0]
        return FormRequest.from_response(response,
                                         meta={'cookiejar': response.meta['cookiejar']},
                                         method='POST',
                                         formdata={'key': key},
                                         dont_click=False,
                                         callback=self.parse_submit)

    def parse_submit(self, response):
        url = response.url
        if not (b'application/pdf' in response.headers['Content-Type']):
            return None

        file_name = str(response.headers['Content-Disposition']).split(';')[1].strip().split("=")[1][:-1]

        with open(os.path.join(TMPDIR, file_name), 'wb') as f:
            f.write(response.body)

        #dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(TMPDIR, file_name).replace('feeder/spiders', '', 1)

        return Source(
            domain=self.domain,
            scraped_at=arrow.utcnow(),
            scraped_url=url,
            file_urls=['file://%s' % os.path.join(TMPDIR, file_name)]
        )

    def clear_tmp(self):
        # Remove items in tmp/
        #dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(TMPDIR, '*').replace('feeder/spiders', '', 1)
        os.system('rm -rf %s' % file_path)

    def __del__(self):
        self.clear_tmp()

    def prepare_url(self, url):
        return ('' + self.base_url + '/' + url).split('&')[0]
