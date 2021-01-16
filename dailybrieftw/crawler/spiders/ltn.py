from datetime import datetime
import re

import scrapy

from .db import url_exists, push_to_db


CRAWL_PAGES = 25


class LtnSpider(scrapy.Spider):
    name = "ltn"

    def start_requests(self):
        url = 'https://news.ltn.com.tw/ajax/breakingnews/all/'
        for i in range(1, CRAWL_PAGES):
            yield scrapy.Request(url=url+str(i), callback=self.parse)

    def parse(self, response):

        json_response = response.json()
        first_page = response.url == 'https://news.ltn.com.tw/ajax/breakingnews/all/1'
        urls = [news['url'] for news in json_response['data']] if first_page \
            else [news['url'] for news in json_response['data'].values()]
        for url in urls:
            if url_exists(url.split('?')[0], 'articles'):
                self.log('[IGNORE]')
                continue
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        url = response.xpath('//link[@rel="canonical"]/@href').get()
        title = response.xpath('//meta[@property="og:title"]/@content').get()
        title = title.split(' - ')[0]
        content = response.xpath('//div[@class="text boxTitle boxText"]/p[not(@*)]/text()').getall()
        if len(content) > 0:
            content[0] = re.sub('^〔.*〕', '',  content[0])
        content = '\n'.join(content)
        crawl_time = datetime.now()
        publish_time = response.xpath('//meta[@property="article:published_time"]/@content').get().split('+')[0]
        push_to_db('articles', self.name, url, title, content, crawl_time, publish_time)
