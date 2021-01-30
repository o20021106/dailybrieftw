from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base

class Article(Base):
    __tablename__ = 'article'
    id = Column(String(255), primary_key=True)
    source = Column(String(50))
    url = Column(String(255))
    title = Column(String(255))
    content = Column(Text)
    crawl_time = Column(DateTime)
    publish_time = Column(DateTime)
    
    def __init__(self, id=None, source=None, url=None, title=None,
                 content=None, crawl_time=None, publish_time=None):
        self.id = id
        self.source = source
        self.url = url
        self.title = title
        self.content = content
        self.crawl_time = crawl_time
        self.publish_time = publish_time

    def __repr__(self):
       return "<Article(source='%s', url='%s', title='%s')>" % (
                            self.source, self.url, self.title)


class Cluster(Base):
    __tablename__ = 'cluster'
    publish_time = Column(DateTime, primary_key=True)
    cluster_num = Column(Integer, primary_key=True)
    cluster_id = Column(Integer, primary_key=True)
    cluster_size = Column(Integer)
    title = Column(String(255))
    content = Column(String(1000))
    source = Column(String(50))

    def __init__(self, publish_time=None, cluster_num=None, cluster_id=None,
                cluster_size=None, title=None, content=None, source=None):
        self.publish_time = publish_time
        self.cluster_num = cluster_num
        self.cluster_id = cluster_id
        self.cluster_size = cluster_size
        self.title = title
        self.content = content
        self.source = source

    def __repr__(self):
       return "<Cluster(publish_time='%s', cluster_num='%s', cluster_id='%s', title='%s')>" % (
                            self.publish_time, self.cluster_num, self.cluster_id, self.title)