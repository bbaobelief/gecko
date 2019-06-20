import json
import scrapy
from lxml import etree
from scrapy.spiders import CrawlSpider
from wispx.items import WispxItem


class WispxSpider(CrawlSpider):
    name = 'wispx'
    allowed_domains = ['wispx.cn']
    start_url = "https://wallpaper.wispx.cn/hot"

    def start_requests(self):
        data = {"page": "1"}
        yield self.next_page(data)

    def parse(self, response):
        resp = json.loads(response.body_as_unicode())
        view = resp['data']['view']
        last_page = resp['data']['page']['last_page']

        html = etree.HTML(view)
        items = html.xpath('//div[@class="item"]')
        item = WispxItem()

        for i in items:
            src = i.xpath('./div[@class="options"]/a[@class="download"]/@href')
            desc = i.xpath('./div[@class="description"]/div/text()')
            alt = i.xpath('./div[@class="avatar"]/div/text()')
            url = "https://wallpaper.wispx.cn{0}".format(i.xpath('./a/@href')[0])

            item['url'] = url
            item['alt'] = alt[0]
            item['src'] = src[0]
            item['desc'] = desc[0]
            yield item

        # 下一页
        for page in range(2, last_page + 1):
            data = {"page": str(page)}
            yield self.next_page(data)

    def next_page(self, data):
        return scrapy.FormRequest(url=self.start_url, formdata=data, headers={'x-requested-with': 'XMLHttpRequest'})
