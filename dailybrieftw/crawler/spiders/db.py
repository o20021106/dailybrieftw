import os
import hashlib

import mysql.connector

def hash_url(url):
    return hashlib.sha256(url.encode('utf-8')).hexdigest()


def get_db_connection():
    db_socket_dir = os.environ.get('DB_SOCKET_DIR', '/cloudsql')
    cloud_sql_connection_name = os.environ['CLOUD_SQL_CONNECTION_NAME']
    print(cloud_sql_connection_name)
    unix_socket = '{}/{}'.format(db_socket_dir, cloud_sql_connection_name)
    return mysql.connector.connect(unix_socket=unix_socket,
                                   user=os.environ['DB_USER'],
                                   password=os.environ['DB_PWD'],
                                   database=os.environ['DB_NAME'])


def url_exists(url, table_name):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    hash_id = hash_url(url)
    cursor.execute(f'SELECT id FROM {table_name} where id="{hash_id}"')
    exists = False
    if len(cursor.fetchall()) > 0:
        exists = True
    cursor.close()
    cnx.close()
    return exists

def push_to_db(table_name, source, url, title, content, crawl_time, publish_time):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    hash_id = hash_url(url)
    if url_exists(url, table_name):
        return
    cursor.execute(f'''INSERT INTO {table_name}
                       (id, source, url, title, content,
                        crawl_time, publish_time)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                   (hash_id, source, url, title, content, crawl_time, publish_time))
    cnx.commit()
    cursor.close()
    cnx.close()
