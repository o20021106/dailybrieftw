import os
import pickle

from sklearn.cluster import DBSCAN

from dailybrieftw.utils.utils import segment


class Cluster():
    def __init__(self, eps=1, min_samples=1, segmenter_type='jieba'):
        model_path = os.environ['tfidf_model_path']
        self.vectorizer = pickle.load(open(model_path, 'rb'))
        self.dbscanner = DBSCAN(eps=eps, min_samples=min_samples)

    def cluster(self, texts):
        segmented_texts = segment(texts)
        vectors = self.vectorizer.transform(segmented_texts)
        labels = self.dbscanner.fit_predict(vectors)
        return labels

    def get_clusters(self, texts):
        labels = self.cluster(texts)
        return labels

    def get_representitive_text(self, texts, max_len=300):
        representitive_text = ''
        for text in texts:
            first_paragraph = text.split('\n')[0]
            if len(first_paragraph) > len(representitive_text) and len(first_paragraph) <= max_len:
                representitive_text = first_paragraph
        if len(representitive_text) == 0 and len(texts) > 0:
            representitive_text = texts[0][:max_len]
        return representitive_text

    def get_first_paragraphs(self, cluster_texts):
        first_paragraphs = []
        for texts in cluster_texts:
            first_paragraph = self.get_representitive_text(texts)
            first_paragraphs.append(first_paragraph)
        return first_paragraphs


if __name__== '__main__':
    import time
    start = time.time()
    cluster = Cluster(segmenter_type='ckiptagger')
    with open('dailybrieftw/cluster/data/texts.txt') as f:
        lines = f.readlines()
    labels, clusters = cluster.get_clusters(lines)
    first_paragraphs = cluster.get_first_paragraphs(clusters)
    for p in first_paragraphs[:10]:
        print(f'===================={len(p)}====================')
        print(p)
    stop = time.time()
    print(stop-start)