import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from divnil.items import WallpaperItem


class DivnilSpider(CrawlSpider):
    name = 'divnil'
    allowed_domains = ['divnil.com']

    rules = [
        Rule(LinkExtractor(allow=r'https://divnil.com/wallpaper/iphone-x/list_\d+.html'), callback='parse_item',
             follow=True),
    ]

    def __init__(self, category='iphone-x', *args, **kwargs):
        super(DivnilSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://divnil.com/wallpaper/%s/' % category]

    def parse_item(self, response):
        pattern = re.compile(r'^【.*】')
        content = response.xpath("//a[@rel='wallpaper']")

        for i in content:
            item = WallpaperItem()
            href = i.xpath(".//@href").extract_first()
            href = '{0}{1}'.format(self.start_urls[0], href)

            alt = i.xpath(".//img/@alt").extract_first()
            alt = re.sub(pattern, '', alt)

            src = i.xpath(
                ".//img/@original|.//img[not(contains(@src,'/wallpaper/img/app/white.png'))]/@src").extract_first()
            src = '{0}{1}'.format(self.start_urls[0], src.replace('_s.', '_raw.'))

            item['alt'] = alt
            item['src'] = src
            item['url'] = href
            yield item
