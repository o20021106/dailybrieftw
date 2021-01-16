import json
import re
from datetime import datetime

import scrapy

from .db import url_exists, push_to_db

class AppleDailySpider(scrapy.Spider):
    name = "appledaily"
    feed_size = 100
    roll_back = 9

    def start_requests(self):
        url_template = 'https://tw.appledaily.com/pf/api/v3/content/fetch/query-feed?query={"feedOffset":%d,"feedQuery":"type:story","feedSize":"%d","sort":"display_date:desc"}&_website=tw-appledaily&filter={content_elements{type,_id,canonical_url,headlines{basic},source{source_id,system,name,source_type}}'
        for i in range(self.roll_back):
            url = url_template % (i * self.feed_size, self.feed_size)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_response = response.json()
        article_api_template = ('https://tw.appledaily.com/pf/api/v3/content/fetch/content-by-id?query={"id":"%s","website_url":"tw-appledaily"}')
        for element in json_response['content_elements']:
            if '_id' not in element:
                continue
            canonical_url = response.urljoin(element['canonical_url'])
            api_url = article_api_template % element['_id']
            if url_exists(canonical_url, 'articles'):
                continue
            yield scrapy.Request(url=api_url, callback=self.parse_page)
    
    def parse_page(self, response):
        json_response = response.json()

        url = response.urljoin(json_response['canonical_url'])
        title = json_response['headlines']['basic']
        content = [element['content']for element in json_response['content_elements']
                   if element['type']=='text']
        content = '\n'.join(content)
        crawl_time = datetime.now()
        publish_time = json_response['publish_date']
        publish_time = datetime.strptime(publish_time[:19], '%Y-%m-%dT%H:%M:%S')
        push_to_db('articles', self.name, url, title, content, crawl_time, publish_time)
