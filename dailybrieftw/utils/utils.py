import os
import logging
import re
import binascii
import collections
import datetime
import hashlib
import sys

import jieba
from google.cloud import storage
from google.oauth2 import service_account
import six
from six.moves.urllib.parse import quote
import google.auth


jieba.set_dictionary('dailybrieftw/utils/model_files/dict.txt.big')


def segment(texts):
    return [' '.join(jieba.cut(text)) for text in texts]
        

def setup_logger(log_file, logger_name=None, level=logging.DEBUG):
    if logger_name is not None:
        logger = logging.getLogger(logger_name)
    else:
        logger = logging.getLogger()
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    fh = logging.FileHandler(log_file)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


def clean(text):
    text = re.sub(r'\([^()]*\)', '',  text)
    text = re.sub(r'\〔[^〕]*\〕', '',  text)
    text = re.sub(r'\[[^\]]*\]', '',  text)
    text = re.sub(r'［[^］]*\］', '',  text)
    text = re.sub(r'\<[^\>]*\>', '',  text)
    text = re.sub(r'【[^】]*】', '',  text)
    text = re.sub(r'（[^）]*）', '',  text)
    return text


def clean_title(text):
    text = clean(text)
    text = re.sub('NBA》', '',  text)
    text = re.sub('中職／', '',  text)
    text = re.sub('影／', '',  text)
    text = re.sub('NBA／', '',  text)
    text = re.sub('PLG／', '',  text)
    text = re.sub('獨／', '',  text)
    text = re.sub('MLB》', '',  text)
    text = re.sub('網球》', '',  text)
    text = re.sub('MLB／', '',  text)
    return text



def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )


def generate_signed_url(bucket, blob_object):
    credentials, project_id = google.auth.default()

    # Perform a refresh request to get the access token of the current credentials (Else, it's None)
    from google.auth.transport import requests
    r = requests.Request()
    credentials.refresh(r)

    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.get_blob(blob_object)
    if blob is None:
        return None
    expires = datetime.datetime.now() + datetime.timedelta(seconds=86400)

    if hasattr(credentials, "service_account_email"):
        service_account_email = credentials.service_account_email
    service_account_email = 'dailybrieftw@dailybrieftw-302512.iam.gserviceaccount.com'
    url = blob.generate_signed_url(expiration=expires,service_account_email=service_account_email, access_token=credentials.token)
    return url