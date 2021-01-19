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
