import os
import hashlib
import logging

from .models import Article, Cluster
from .database import db_session

from dailybrieftw.utils.utils import setup_logger


logger = logging.getLogger()


def hash_url(url):
    return hashlib.sha256(url.encode('utf-8')).hexdigest()


def url_exists(url):
    hash_id = hash_url(url)
    article = Article.query.get(hash_id)
    return True if article else False


def push_article_to_db(source, url, title, content, crawl_time, publish_time):
    hash_id = hash_url(url)

    if not url_exists(url):
        article = Article(id=hash_id, source=source, url=url, title=title,
                          content=content, crawl_time=crawl_time,
                          publish_time=publish_time)
        try:
            db_session.add(article)
            logger.info(f'[DATABSE][PUSH] {url} to database.')
            db_session.commit()
        except:
            logger.exception('[DATABASE][PUSH] failed.')

