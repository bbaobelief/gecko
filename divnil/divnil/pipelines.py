import os
import json
import codecs
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class JsonPipeline(object):

    def process_item(self, item, spider):
        base_dir = os.getcwd()
        filename = base_dir + '/{0}.json'.format(spider.name)
        with codecs.open(filename, 'a') as f:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            f.write(line)
        return item


class DivnilPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        src = item['src']
        yield scrapy.Request(src)
