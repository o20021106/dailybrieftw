import os
import logging
import re

import jieba

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
