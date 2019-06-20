import scrapy


class WallpaperItem(scrapy.Item):

    url = scrapy.Field()
    src = scrapy.Field()
    alt = scrapy.Field()
