import json
import scrapy
from datetime import datetime

class Bao24hCrawler(scrapy.Spider):
    name = 'bao24h'
    allowed_domains = ['24h.com.vn']
    start_urls =    ['https://www.24h.com.vn/']
    count = 0
    def parse(self, response):
        if response.status == 200 and response.css('meta[property="og:type"]::attr("content")').get() == 'article':
            
            Bao24hCrawler.count += 1
            print(Bao24hCrawler.count)

            data = {
                'link': response.url,
                'title': response.css('h1.clrTit.bld.tuht_show::text').get(),
                'description': response.css('h2.ctTp.tuht_show::text').get(),
                'content': '\n'.join([
                    ''.join(c.css('*::text').getall())
                        for c in response.css('article[id="article_body" ] > p')
                ]),
                'category': response.css('a.brmItem.bld span::text').get(),
                'date': response.css('div.updTm.updTmD.mrT5::text').get(),
                'keywords': [
                    k.strip() for k in response.css('meta[name="keywords"]::attr("content")').get().split(',')
                ],

            }

            with open('bao24h.txt', 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')

        yield from response.follow_all(css='a[href^="https://www.24h.com.vn/"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)
