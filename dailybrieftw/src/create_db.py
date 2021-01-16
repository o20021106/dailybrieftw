import os

import mysql.connector


def get_db_connection(**config):
    return mysql.connector.connect(**config)


def create_db(db_name):
    cnx = get_db_connection(host=os.environ['DB_HOST'], user=os.environ['DB_USER'],
                            password=os.environ['DB_PWD'])
    cursor = cnx.cursor()
    cursor.execute(f'CREATE DATABASE {db_name}')


def create_table(db_name, table_name):
    cnx = get_db_connection(host=os.environ['DB_HOST'],
                            user=os.environ['DB_USER'],
                            password=os.environ['DB_PWD'],
                            database=db_name)
    cursor = cnx.cursor()
    cursor.execute(f'CREATE TABLE {table_name} (id VARCHAR(255) PRIMARY KEY, '
                   'source VARCHAR(50), '
                   'url VARCHAR(255), title VARCHAR(255), content TEXT, '
                   'crawl_time DATETIME, publish_time DATETIME)')

def create_index(db_name, table_name):
    cnx = get_db_connection(user=os.environ['DB_USER'],
                            password=os.environ['DB_PWD'],
                            database=db_name)
    cursor = cnx.cursor()
    cursor.execute(f'CREATE INDEX publish_time ON {table_name} (publish_time)')
    cursor.execute(f'CREATE INDEX publish_time ON {table_name} (crawl_time)')

if __name__ == '__main__':
    create_db('dailybrief')
    create_table('dailybrief', 'articles')
