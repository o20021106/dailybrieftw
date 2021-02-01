import json
import re
from datetime import datetime

import scrapy

from dailybrieftw.utils.database_ops import url_exists, push_article_to_db
from dailybrieftw.utils.utils import clean, clean_title, get_current_local_time


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
            url = response.urljoin(element['canonical_url'])
            api_url = article_api_template % element['_id']
            if url_exists(url):
                self.log(f'[IGNORE] {url}')
                continue
            yield scrapy.Request(url=api_url, callback=self.parse_page)
    
    def parse_page(self, response):
        json_response = response.json()

        url = response.urljoin(json_response['canonical_url'])
        title = json_response['headlines']['basic']
        title = '' if title is None else clean_title(title)

        content = [element['content']for element in json_response['content_elements']
                   if element['type']=='text']
        content = [clean(text.replace('\n', ' ')) for text in content]
        content = '\n'.join([text for text in content if len(text) > 0])
        crawl_time = get_current_local_time()
        try:
            publish_time = json_response['publish_date']
            publish_time = datetime.strptime(publish_time[:19], '%Y-%m-%dT%H:%M:%S')
        except KeyError:
            publish_time = crawl_time
        try:
            push_article_to_db(self.name, url, title, content, crawl_time, publish_time)
        except:
            self.log('error', url)