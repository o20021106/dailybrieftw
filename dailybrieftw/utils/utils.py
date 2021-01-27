import os
import logging
import re

import jieba
from google.cloud import storage


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
