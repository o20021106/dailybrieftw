from datetime import datetime

import scrapy

from dailybrieftw.utils.database_ops import url_exists, push_article_to_db
from dailybrieftw.utils.utils import clean, clean_title


CRAWL_PAGES = 30


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
            if url_exists(url_):
                self.log(f'[IGNORE] {url}')
                continue
            yield scrapy.Request(url=response.urljoin(url_), callback=self.parse_page)

    def parse_page(self, response):
        url = response.xpath('//meta[@property="og:url"]/@content').get()
        title = response.xpath('//h1[@class="article-content__title"]/text()').get()
        title = '' if title is None else clean_title(title)
        content = response.xpath('//section[@class="article-content__editor "]'
                                 '/p[not(@*)]/text()').getall()
        content = [clean(text.replace('\n', ' ')) for text in content]
        content = '\n'.join([text for text in content if len(text) > 0])
        crawl_time = datetime.now()
        publish_time = response.xpath('//meta[@name="date"]'
                                 '/@content').get()
        if publish_time is None:
            publish_time = crawl_time
        else:
            try:
                publish_time = datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                publish_time = crawl_time
        try:
            push_article_to_db(self.name, url, title, content, crawl_time, publish_time)
        except:
            self.log('error', url)
