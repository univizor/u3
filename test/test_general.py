import unittest
from feeder.items import Source
from arrow import utcnow
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy import *
from sqlalchemy import func
from feeder.models import *

DOMAIN = 'univizor.si'
SCRAPED_AT = utcnow()
SCRAPED_URL = 'http://univizor.si'
FILES = ["README.md"]
FILE_URLS = ['file://%s' % FILES[0]]


def build_source(args=None):
    if args is None:
        args = {}

    defaults = {
        'domain': DOMAIN,
        'scraped_at': SCRAPED_AT,
        'scraped_url': SCRAPED_URL,
        'files': FILES,
        'file_urls': FILE_URLS
    }

    return Source(**{**defaults, **args})


class ItemsTest(unittest.TestCase):
    def test_structure(self):
        item = build_source()
        self.assertEqual(item['domain'], DOMAIN)
        self.assertEqual(item['scraped_at'], SCRAPED_AT)
        self.assertEqual(item['scraped_url'], SCRAPED_URL)
        self.assertEqual(item['files'], FILES)
        self.assertEqual(item['file_urls'], FILE_URLS)
        self.assertEqual(len(item.keys()), 5)


class ModelsTest(unittest.TestCase):
    Session = None

    def setUp(self):
        engine = self.db_connect()
        Base.metadata.drop_all(engine, checkfirst=True)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def db_connect(self):
        return create_engine('sqlite:///:memory:', echo=False)

    def test_dbsource(self):
        source = DBSource(**build_source())
        self.assertEqual(source.domain, DOMAIN)

    def test_repository(self):
        source = DBSource(**build_source({'scraped_at': None}))
        repository = self.Session()
        repository.add(source)
        repository.commit()

        result = repository.query(func.count(DBSource.id)).count()
        self.assertEqual(1, result)


if __name__ == '__main__':
    unittest.main()
