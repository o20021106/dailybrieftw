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

def crawl_news():
    process = CrawlerProcess(settings=spider_setting)
    process.crawl(LtnSpider)
    #process.crawl(AppleDailySpider)
    #process.crawl(ChinaTimesSpider)
    #process.crawl(UdnSpider)
    process.start()


if __name__ == '__main__':
    crawl_news()