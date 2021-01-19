import subprocess
from datetime import datetime, timedelta
from collections import Counter, OrderedDict
import time
import os
import logging

import crochet
crochet.setup()
from flask import Flask, request, jsonify
from flask import Blueprint
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging, DEFAULT_LOGGING

from dailybrieftw.cluster.cluster import Cluster
from dailybrieftw.utils.models import Article
from dailybrieftw.crawler.spiders import LtnSpider, UdnSpider, AppleDailySpider, ChinaTimesSpider
from dailybrieftw.utils.database_ops import push_cluster_to_db


clusterer = Cluster()

DEFAULT_LOGGING['loggers']['twisted']['level'] = 'DEBUG'
setting = {'ROBOTSTXT_OBBEY': True,
           'LOG_LEVEL': logging.DEBUG,
           'LOG_ENABLED': True}
crawl_runner = CrawlerRunner(setting)
configure_logging(setting)


logger = logging.getLogger()
bp = Blueprint('endpoints', __name__)


@bp.route('/crawl', methods=['GET'])
def crawl():
    logger.info('[CRAWL] start')
    eventual = scrape_with_crochet(LtnSpider)
    eventual = scrape_with_crochet(UdnSpider)
    eventual = scrape_with_crochet(AppleDailySpider)
    eventual = scrape_with_crochet(ChinaTimesSpider)
    logger.info('[CRAWL] done')
    return ('', 204)


@crochet.wait_for(timeout=240.0)
def scrape_with_crochet(spider):
    logger.info(f'[CRAWL] start crawing {spider.name}')
    eventual = crawl_runner.crawl(spider)
    return eventual
    

@bp.route('/', methods=['GET'])
def hello():
    return 'Hello world.'
