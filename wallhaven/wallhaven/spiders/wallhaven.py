# -*- coding: utf-8 -*-

import scrapy
from urllib.parse import urlencode
from scrapy.spiders import CrawlSpider
from wallhaven.items import WallhavenItem


class WallhavenSpider(CrawlSpider):
    name = 'wallhaven'
    allowed_domains = ['wallhaven.cc']
    start_url = "https://wallhaven.cc/search?"
    params = {
        "atleast": "1920x1080",
        "categories": "100",
        "purity": "100",
        "sorting": "toplist",
        "topRange": "1y",
        "order": "asc"
    }

    def start_requests(self):

        # 从第二页获取总页数
        for page in range(1, 3):
            data = {"page": str(page)}
            yield self.next_page(dict(self.params, **data))


    def parse(self, response):

        links = response.xpath(r"/html/body/main/div/section/ul/li/figure/a/@href").extract()

        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_item)

        # 下一页
        match_page = response.xpath(r"/html/body/main/div/section/header/h2/span[text()='2']/../text()").extract()
        if match_page:
            last_page = match_page[-1].split(' / ')[-1]
            for page in range(3, int(last_page) + 1):
                data = {"page": str(page)}
                yield self.next_page(dict(self.params, **data))

    def parse_item(self, response):
        src = response.xpath(r"//img[@id='wallpaper']/@src").extract_first()
        alt = response.xpath(r"//ul[@id='tags']/li/a[@class='tagname']/text()").extract()
        url = response.xpath(r"//input[@id='wallpaper-short-url-copy']/@value").extract_first()

        item = WallhavenItem()
        item['url'] = url
        item['alt'] = ','.join(alt)
        item['src'] = src
        yield item

    def next_page(self, params):
        url = self.start_url + urlencode(params)
        return scrapy.Request(url=url)
