# -*- coding: utf-8 -*-
import os
from gensim.models import KeyedVectors
import numpy as np


class GensimEmbedding:

    def __init__(self, vec_path='', cache_vec_path='', logger=None):
        self.vec_path = vec_path
        self.cache_vec_path = cache_vec_path
        self.logger = logger
        self._load_vec()
        self._load_cache_vec()

    def _load_vec(self):
        if os.path.exists(self.vec_path):
            print(os.path.splitext(self.vec_path))
            if os.path.splitext(self.vec_path)[-1] == ".model":
                self.w2v = KeyedVectors.load(self.vec_path)
            else:
                self.w2v = KeyedVectors.load_word2vec_format(self.vec_path, binary=False)
            if self.logger:
                self.logger.info("Step One: load w2v file successful!")
        else:
            if self.logger:
                self.logger.warning("Step X: the w2v file not exists ! ")
            raise FileNotFoundError("The w2v file is not exists ! ")

    def _load_cache_vec(self):
        if os.path.exists(self.cache_vec_path):
            # self.cache_vec = zload(self.cache_vec_path)
            pass
        else:
            self.cache_vec = {}

    def new_vector(self, v):
        return v if v is not None else np.random.randn(self.w2v.vector_size)

    def __getitem__(self, word):
        v = None
        if word is None:
            return None
        if word in self.cache_vec:
            return self.cache_vec[word]
        if word in self.w2v:
            v = self.w2v[word]
        v = self.new_vector(v)
        self.cache_vec[word] = v
        return v

    def __contains__(self, word):
        return word in self.w2v

    @property
    def vector_size(self):
        return self.w2v.vector_size


class FunctionEmbedding:

    def __init__(self, vec_path='', cache_vec_path='', logger=None):
        self.vec_path = vec_path
        self.cache_vec_path = cache_vec_path
        self.logger = logger
        self.w2v = dict()
        self._load_vec()
        self._load_cache_vec()

    def _load_vec(self):
        if os.path.exists(self.vec_path):
            for line in open(self.vec_path, encoding='utf8'):
                query, vec = line.strip().split('\t')
                self.w2v[query] = np.array([float(ii) for ii in vec.split(',')])
            self.length = len(self.w2v)
            self.vector_size = len(vec.split(','))

    def _load_cache_vec(self):
        if os.path.exists(self.cache_vec_path):
            # self.cache_vec = zload(self.cache_vec_path)
            pass
        else:
            self.cache_vec = {}

    def new_vector(self, v):
        return v if v is not None else np.zeros(self.vector_size)

    def __getitem__(self, word):
        v = None
        if word is None:
            return None
        if word in self.cache_vec:
            return self.cache_vec[word]
        if word in self.w2v:
            v = self.w2v[word]
        v = self.new_vector(v)
        self.cache_vec[word] = v
        return v

    def __contains__(self, word):
        return word in self.w2v

    # @property
    # def vector_size(self):
        # return self.vector_size

if __name__ == '__main__':
    emb = FunctionEmbedding('embedding/vec_.txt')
    print(f"vector_size: {emb.vector_size}")
    emb = GensimEmbedding('embedding/word2vec.model')
    print(f"vector_size: {emb.vector_size}")
