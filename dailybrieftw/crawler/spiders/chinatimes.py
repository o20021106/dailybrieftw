from datetime import datetime

import scrapy

from .db import url_exists, push_to_db


CRAWL_PAGES = 11


class ChinaTimesSpider(scrapy.Spider):
    name = "chinatimes"

    def start_requests(self):
        url = 'https://www.chinatimes.com/newspapers/2601?page={}'
        for i in range(1, CRAWL_PAGES):
            yield scrapy.Request(url=url.format(i), callback=self.parse)

    def parse(self, response):

        urls = response.xpath('//ul[@class="vertical-list list-style-none"]'
                              '/li//div[@class="col"]/h3/a/@href').getall()
        for url in urls:
            url = response.urljoin(url)
            if url_exists(url.split('?')[0], 'articles'):
                self.log('[IGNORE]')
                continue
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        url = response.xpath('//link[@rel="canonical"]/@href').get()
        title = response.xpath('//h1[@class="article-title"]/text()').get()
        content = response.xpath('//div[@class="article-body"]/p[not(@*)]/text()').getall()
        content = '\n'.join(content)
        crawl_time = datetime.now()
        publish_time = response.xpath('//meta[@property="article:published_time"]/@content').get().split('+')[0]
        push_to_db('articles', self.name, url, title, content, crawl_time, publish_time)
