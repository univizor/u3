from scrapy import Item, Field


class Source(Item):
    domain = Field()
    scraped_at = Field()
    scraped_url = Field()
    files = Field()
    file_urls = Field()
