# -*- coding: utf-8 -*-

import scrapy


class WallhavenItem(scrapy.Item):

    url = scrapy.Field()
    src = scrapy.Field()
    alt = scrapy.Field()
