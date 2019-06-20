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

        content = response.xpath("/html/body/main/div/section/ul/li")

        for i in content:
            item = WallhavenItem()
            data_src = i.xpath(r".//figure/img/@data-src").extract_first().split('/')
            data_href = i.xpath(r".//figure/a/@href").extract_first()
            resolution = i.xpath(r".//figure/div/span/text()").extract_first()
            src = "https://w.wallhaven.cc/full/{0}/wallhaven-{1}".format(data_src[-2], data_src[-1])

            item['url'] = data_href
            item['alt'] = resolution
            item['src'] = src
            yield item

        # 下一页
        match_page = response.xpath(r"/html/body/main/div/section/header/h2/span[text()='2']/../text()").extract()
        if match_page:
            last_page = match_page[-1].split(' / ')[-1]
            for page in range(3, int(last_page) + 1):
                data = {"page": str(page)}
                yield self.next_page(dict(self.params, **data))

    def next_page(self, params):
        url = self.start_url + urlencode(params)
        return scrapy.Request(url=url)
