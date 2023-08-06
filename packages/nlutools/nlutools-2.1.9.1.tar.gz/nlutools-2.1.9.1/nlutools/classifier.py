from collections import defaultdict

import numpy as np
from scipy.spatial.distance import cosine
from sklearn.metrics import pairwise_distances

from nlutools.nlu import NLU


class Classifier(object):
    def __init__(self, corpus_path="", center_dict={}, dim=512):
        self.nlu = NLU(verbose=False)
        self.dim = dim
        self.class_dict = defaultdict(list)
        self.corpus = corpus_path
        if not corpus_path and not center_dict:
            print("Init fail! Please pass in `corpus_path` or `center_dict`")
        else:
            if center_dict:
                self.center_dict = center_dict
                self._build_centers(False)
            else:
                self.center_dict = {}
                print("Building model, please wait...")
                self._build_centers(True)

    def normalize(self, v):
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        return v / norm

    def _build_centers(self, build=False):
        if build:
            with open(self.corpus, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                lines = [x.strip().split('\t') for x in lines]
                for line in lines:
                    self.class_dict[line[1]].append(line[0])
                for k, v in self.class_dict.items():
                    embs = np.asarray(self._get_embs(v))
                    center = np.mean(embs, axis=0).squeeze()
                    self.center_dict[k] = center
        tps = list(self.center_dict.items())
        self.centers = [x[1] for x in tps]
        self.classes = [x[0] for x in tps]

    def infer_by_input(self):
        while True:
            sent = input("enter a sentence: ")
            res, pclass = self.infer(sent)
            print(res)
            print("predicted class: {}".format(pclass))

    def infer(self, sent, show_dist=True):
        if isinstance(sent, str):
            results, preds = self._pred_class(sent)
        elif isinstance(sent, list):
            if len(sent) > 1:
                results, preds = self.infer_sents(sent)
            else:
                results, preds = self._pred_class(sent)
        else:
            results = None
            preds = None
            print("Only support `str` and `list` input type")
        if show_dist:
            return results, preds
        else:
            return preds

    def infer_sents(self, sents):
        embs = self._get_embs(sents)
        dists = np.asarray(pairwise_distances(embs, self.centers, metric='cosine'))
        preds = np.argmin(dists, axis=-1).squeeze()
        preds = [self.classes[x] for x in preds]
        results = [list(zip(self.classes, dist)) for dist in dists]
        return results, preds

    def _get_embs(self, sent):
        return self.nlu.bert_encode(sent, "common", False)['vec']

    def _pred_class(self, sent):
        emb = self._get_embs(sent)
        dists = [cosine(emb, center) for center in self.centers]
        maxind = np.argmin(dists)
        results = list(zip(self.classes, dists))
        return results, self.classes[maxind]
