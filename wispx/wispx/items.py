# -*- coding: utf-8 -*-
import scrapy


class WispxItem(scrapy.Item):
    url = scrapy.Field()
    src = scrapy.Field()
    alt = scrapy.Field()
    desc = scrapy.Field()
