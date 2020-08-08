import json
import scrapy
from datetime import datetime


class TheGioiDiDongSpider(scrapy.Spider):
    name = 'thegioididongCrawler'
    allowed_domains = ['thegioididong.com']
    start_urls = ['https://www.thegioididong.com/']
    COUNT = 0

    def parse(self, response):
        if response.status == 200 and response.css('section.type0 > div::attr(id)').get() == 'normalproduct':
            TheGioiDiDongSpider.COUNT+=1
            print(TheGioiDiDongSpider.COUNT)
            data = {
            
                'link': response.url,
                'category': response.css('ul.breadcrumb > li > a::text')[1].get(),
                'name': response.css('div.rowtop > h1::text').get(),
                'img_url': response.css('div.icon-position > img::attr(src)').getall(),
                'brand': response.css('li.brand > a::text').get(),
                'price':response.css('div.area_price > strong::text').get(),
                'short_desc': '\n'.join([
                    ''.join(c.css('*::text').getall())
                        for c in response.css('article.area_article > h2')]),
            }

            with open('thegioididong.txt', 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')

        yield from response.follow_all(css='a[href^="https://www.thegioididong.com"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)