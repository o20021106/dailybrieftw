import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_user = os.environ['DB_USER']
db_pwd = os.environ['DB_PWD']
db_name = os.environ['DB_NAME']
db_socket_dir = os.environ.get('DB_SOCKET_DIR', '/cloudsql')
cloud_sql_connection_name = os.environ['CLOUD_SQL_CONNECTION_NAME']
uri = (f'mysql+pymysql://{db_user}:{db_pwd}'
       f'@/{db_name}?unix_socket={db_socket_dir}'
       f'/{cloud_sql_connection_name}')
engine = create_engine(uri, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)
