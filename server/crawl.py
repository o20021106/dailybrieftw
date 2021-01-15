import argparse

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from dailybrieftw.crawler.spiders import *


spider_setting = Settings()
spider_setting.set('ROBOTTXT_OBEY', True)
spider_selector = {
    'ltn': LtnSpider,
    'appledaily': AppleDailySpider,
    'chinatimes': ChinaTimesSpider,
    'udn': UdnSpider
}

def crawl_news(source):
    if source in spider_selector:
        process = CrawlerProcess(settings=spider_setting)
        process.crawl(spider_selector[source])
        process.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str)
    args = parser.parse_args()
    crawl_news(args.source)