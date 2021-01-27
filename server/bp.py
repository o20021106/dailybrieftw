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
import soundfile as sf
import numpy as np

from dailybrieftw.cluster.cluster import Cluster
from dailybrieftw.utils.models import Article
from dailybrieftwl.utils.utils import upload_blob
from dailybrieftw.crawler.spiders import LtnSpider, UdnSpider, AppleDailySpider, ChinaTimesSpider
from dailybrieftw.utils.database_ops import push_cluster_to_db
from dailybrieftw.tts.tts import TTS


clusterer = Cluster()
tts = TTS()

DEFAULT_LOGGING['loggers']['twisted']['level'] = 'DEBUG'
setting = {'ROBOTSTXT_OBBEY': True,
           'LOG_LEVEL': logging.DEBUG,
           'LOG_ENABLED': True}
crawl_runner = CrawlerRunner(setting)
configure_logging(setting)

source_mapping = {'ltn': '自由時報', 'appledaily': '蘋果日報',
                  'chinatimes': '中國時報', 'udn': '聯合報'}

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


@bp.route('/cluster', methods=['GET'])
def cluster():
    logger.info(f'[CLUSTER] start clustering')
    crawl_time = datetime.now() - timedelta(days=1)
    crawl_time = datetime(crawl_time.year, crawl_time.month,
                          crawl_time.day, crawl_time.hour)
    articles = Article.query.with_entities(
        Article.title, Article.content, Article.source).filter(Article.publish_time >= crawl_time).all()
    texts = []
    for title, content, _ in articles:
        title = title if title else ''
        content = content if content else ''
        texts.append(title + ' ' + content)
    labels = clusterer.get_clusters(texts)
    label_counts = Counter(labels).most_common()
    clusters = OrderedDict()
    for label, _ in label_counts:
        if label == -1:
            continue
        clusters[label] = []
    for article, label in zip(articles, labels):
        if label == -1:
            continue
        clusters[label].append(article)
    final_cluster_result = []
    for index, cluster in enumerate(clusters.values()):
        if index >= 15:
            break
        title, content, source = cluster[0]
        content = content.split('\n')[0]
        content = content if len(content) <= 500 else content[:500]
        final_cluster_result.append((title, content, source))
        push_cluster_to_db(crawl_time, 0, index, len(cluster), title, content, source)
    cluster_to_tts(final_cluster_result, './tmp/audio.wav')
    audio_prefix = f'{crawl_time.year}_{crawl_time.month}_{crawl_time.day}_0'
    upload_blob('dailybrief', './tmp/audio.wav', f'audio/{audio_prefix}.wav')
    os.remove('./tmp/audio.wav')
    return ('', 204)


def cluster_to_text(cluster_content):
    texts = []
    for index, (title, content, source) in enumerate(cluster_content):
        index += 1
        unit_digit = index % 10
        ten_digit = index // 10
        ten_digit = '十' if ten_digit > 0 else ''
        num = f'{ten_digit}{unit_digit}'
        text = f'第{num}則，，{title}。{content}。{source_mapping[source]}報導。'
        texts.append(text)
    return texts


def cluster_to_tts(cluster_content, audio_file_path):
    texts = cluster_to_text(cluster_content)
    audios = []
    for text in texts:
        _, _, audio = tts.do_synthesis(xtext, simplified=False)
        audios.append(audio)
    audios = np.concatenate(audios)
    sf.write(audio_file_path, audios, 22050, 'PCM_16')
    return


@bp.route('/', methods=['GET'])
def hello():
    return 'Hello world.'
