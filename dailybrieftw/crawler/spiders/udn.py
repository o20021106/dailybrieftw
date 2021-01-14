from datetime import datetime

import scrapy

from .db import url_exists, push_to_db

CRAWL_PAGES = 15


class UdnSpider(scrapy.Spider):
    name = "udn"

    def start_requests(self):
        url = 'https://udn.com/api/more?page={}&id=&channelId=1&cate_id=0&type=breaknews'
        for i in range(CRAWL_PAGES):
            yield scrapy.Request(url=url.format(i), callback=self.parse_list)

    def parse_list(self, response):
        json_response = response.json()
        urls = [news['titleLink'] for news in json_response['lists']]
        for url in urls:
            url = response.urljoin(url)
            url_ = url.split('?')[0]
            if url_exists(url_, 'articles'):
                self.log('[IGNORE]')
                continue
            yield scrapy.Request(url=response.urljoin(url_), callback=self.parse_page)

    def parse_page(self, response):
        url = response.xpath('//meta[@property="og:url"]/@content').get()
        title = response.xpath('//h1[@class="article-content__title"]/text()').get()
        content = response.xpath('//section[@class="article-content__editor "]'
                                 '/p[not(@*)]/text()').getall()
        crawl_time = datetime.now()
        publish_time = response.xpath('//meta[@name="date"]'
                                 '/@content').get()
        content = '\n'.join(content)
        push_to_db('articles', self.name, url, title, content, crawl_time, publish_time)
