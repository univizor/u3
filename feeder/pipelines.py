# -*- coding: utf-8 -*-
import hashlib
import os
import os.path
from feeder.models import *
from sqlalchemy.orm import sessionmaker
from scrapy.pipelines.files import FilesPipeline
from feeder.settings import *


class FeederPipeline(object):
    def __init__(self):
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        repository = self.Session()

        if item.get('images'):
            item['images'] = [i['path'] for i in item.get('images')]

        if item.get('files'):
            item['files'] = [i['path'] for i in item.get('files')]

        source = DBSource(**item)

        try:
            repository.add(source)
            repository.commit()
        except:
            repository.rollback()
            raise
        finally:
            repository.close()

        return item


def custom_file_path(self, request, response=None, info=None):
    url = '' + request.url
    media_guid = ''

    if HASHING_ALGORITHM is 'sha256':
        media_guid = hashlib.sha256(url.encode('utf-8')).hexdigest()
    else:
        media_guid = hashlib.sha1(url.encode('utf-8')).hexdigest()

    media_ext = os.path.splitext(url)[1]

    if not media_ext[1:].isalpha():
        media_base_url = url.split('?', 1)[0]
        media_ext = os.path.splitext(media_base_url)[1]
        if media_ext == '.php':
            media_ext += '.pdf'

    return '%s%s' % (media_guid, media_ext)


FilesPipeline.file_path = custom_file_path
