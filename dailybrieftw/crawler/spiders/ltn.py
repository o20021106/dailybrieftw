import os
from datetime import datetime
import re

import scrapy

from dailybrieftw.utils.database_ops import url_exists, push_article_to_db
from dailybrieftw.utils.utils import clean, clean_title, get_current_local_time


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
            if url_exists(url.split('?')[0]) \
                or url_exists(url.replace('http', 'https').split('?')[0]):
                self.log(f'[IGNORE] {url}')
                continue
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        url = response.xpath('//link[@rel="canonical"]/@href').get()
        url = url if url is not None else response.request.url
        title = response.xpath('//meta[@property="og:title"]/@content').get()
        if title is None:
            title = ''
        else:
            title = title.split(' - ')[0]
            title = clean_title(title)
        content = response.xpath(
            '//div[contains(@class, "boxTitle boxText")]/p[not(@*)]/text()').getall()
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