from datetime import datetime

import scrapy

from dailybrieftw.utils.database_ops import url_exists, push_article_to_db
from dailybrieftw.utils.utils import clean, clean_title, get_current_local_time


CRAWL_PAGES = 11


class ChinaTimesSpider(scrapy.Spider):
    name = "chinatimes"

    def start_requests(self):
        url = 'https://www.chinatimes.com/newspapers/2601?page={}'
        for i in range(1, CRAWL_PAGES):
            yield scrapy.Request(url=url.format(i), callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//ul[@class="vertical-list list-style-none"]/'
        'li//div[@class="col"]/h3/a/@href').getall()
        for url in urls:
            url = response.urljoin(url)
            if url_exists(url.split('?')[0]):
                self.log(f'[IGNORE] {url}')
                continue
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        url = response.xpath('//link[@rel="canonical"]/@href').get()
        title = response.xpath('//h1[@class="article-title"]/text()').get()
        title = '' if title is None else clean_title(title)
        content = response.xpath('//div[@class="article-body"]/p[not(@*)]/text()').getall()
        content = [clean(text.replace('\n', ' ')) for text in content]
        content = '\n'.join([text for text in content if len(text) > 0])
        crawl_time = get_current_local_time()
        publish_time = response.xpath('//meta[@property="article:published_time"]/@content').get()
        if publish_time is None:
            publish_time = crawl_time
        else:
            try:
                publish_time = publish_time[:19]
                publish_time = datetime.strptime(publish_time, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                publish_time = crawl_time
        try:
            push_article_to_db(self.name, url, title, content, crawl_time, publish_time)
        except:
            self.log('error', url)