from scrapy import Request
from feeder.items import Source
import arrow
from feeder.spiders.rul import RUL
import math
from scrapy.http import FormRequest
import os, glob
from slugify import slugify
from feeder.settings import TEMP_FILES_FOLDER


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
        self.clear_temp()
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
        file_name = slugify(file_name, to_lower=True) \
            .replace('-pdf', '.pdf', 1) \
            .replace('-doc', '.doc', 1)

        temp_path = os.path.join(TEMP_FILES_FOLDER, file_name)

        # Writes content to "TEMP_DIR"
        with open(temp_path, 'wb+') as f:
            f.write(response.body)

        return Source(
            domain=self.domain,
            scraped_at=arrow.utcnow(),
            scraped_url=url,
            file_urls=['file://%s' % temp_path]
        )

    def clear_temp(self):
        """ Removes items in TEMP_DIR """
        file_path = os.path.join(TEMP_FILES_FOLDER, '*')
        files = glob.glob(file_path)
        for file_name in files:
            os.unlink(file_name)

    def __del__(self):
        self.clear_temp()

    def prepare_url(self, url):
        return ('' + self.base_url + '/' + url).split('&')[0]
