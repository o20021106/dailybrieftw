from datetime import datetime, timedelta
from collections import Counter, OrderedDict
import os
import logging
import json

import crochet
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging, DEFAULT_LOGGING
import soundfile as sf
import numpy as np
import pytz

from dailybrieftw.cluster.cluster import Cluster as Clusterer
from dailybrieftw.utils.models import Article, Cluster
from dailybrieftw.utils.utils import upload_blob, generate_signed_url
from dailybrieftw.crawler.spiders import (
    LtnSpider, UdnSpider,
    AppleDailySpider, ChinaTimesSpider
)
from dailybrieftw.utils.database_ops import push_cluster_to_db
from dailybrieftw.tts.tts import TTS

crochet.setup()
clusterer = None
tts = None

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
    global clusterer
    if clusterer is None:
        clusterer = Clusterer()
    logger.info(f'[CLUSTER] start clustering')
    now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
    logger.debug(f'[Cluster] current time {now}')
    now = now.astimezone(tz=pytz.timezone('Asia/Taipei'))
    now = datetime(now.year, now.month, now.day)
    logger.info(f'[Cluster] local time {now}')
    crawl_time = now - timedelta(days=1)
    articles = Article.query.with_entities(
        Article.title, Article.content, Article.source).filter(
            Article.publish_time >= crawl_time).all()
    articles_ = []
    for title, content, source in articles:
        title = title if title else ''
        content = content if content else ''
        source = source if source else ''
        articles_.append((title, content, source))
    articles = articles_
    del articles_
    labels = clusterer.get_clusters(
        [title + ' ' + content for title, content, _ in articles])
    label_counts = Counter(labels).most_common()
    clusters = OrderedDict((label, []) for label, _ in label_counts if label != -1)
    for article, label in zip(articles, labels):
        if label != -1:
            clusters[label].append(article)
    final_cluster_result = []
    for cluster in clusters.values():
        if len(final_cluster_result) >= 15:
            break
        for title, content, source in cluster:
            content = content.split('\n')[0]
            if len(content) > 50:
                break
        if len(content) < 50:
            continue
        content = content if len(content) <= 500 else content[:500]
        final_cluster_result.append((title, content, source))
        push_cluster_to_db(now, 0, len(final_cluster_result),
                           len(cluster), title, content, source)
    cluster_to_tts(final_cluster_result, './tmp/audio.wav')
    audio_prefix = now.strftime('%Y_%m_%d_0')
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
    global tts
    if tts is None:
        tts = TTS()
    texts = cluster_to_text(cluster_content)
    audios = []
    for text in texts:
        _, _, audio = tts.do_synthesis(text, simplified=False)
        audios.append(audio)
    audios = np.concatenate(audios)
    sf.write(audio_file_path, audios, 22050, 'PCM_16')
    return
