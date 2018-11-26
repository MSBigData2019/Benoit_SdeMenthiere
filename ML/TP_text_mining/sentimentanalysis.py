# Authors: Alexandre Gramfort
#          Chloe Clavel
# License: BSD Style.
# TP Cours ML Telecom ParisTech MDI343

import os.path as op
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin

###############################################################################
# Load data
print("Loading dataset")

from glob import glob
filenames_neg = sorted(glob(op.join('.', '34data', 'data', 'imdb1', 'neg', '*.txt')))
filenames_pos = sorted(glob(op.join('.', '34data', 'data', 'imdb1', 'pos', '*.txt')))

texts_neg = [open(f).read() for f in filenames_neg]
texts_pos = [open(f).read() for f in filenames_pos]
texts = texts_neg + texts_pos
y = np.ones(len(texts), dtype=np.int)
y[:len(texts_neg)] = 0.

print("%d documents" % len(texts))

###############################################################################
# Start part to fill in

def count_words(texts):
    """Vectorize text : return count of each word in the text snippets

    Parameters
    ----------
    texts : list of str
        The texts

    Returns
    -------
    vocabulary : dict
        A dictionary that points to an index in counts for each word.
    counts : ndarray, shape (n_samples, n_features)
        The counts of each word in each text.
        n_samples == number of documents.
        n_features == number of words in vocabulary.
    """
    words = set()
    vocabulary = {}
    i = 0
    for text in texts:
        words_text = text.split()
        words.update(words_text)
        dicts.append(dict(zip(unique, count)))
    for text in texts:
        unique, count = np.unique(words_text, return_counts=True)
    n_features = len()
    counts = np.zeros((len(texts), n_features))
    return vocabulary, counts


class NB(BaseEstimator, ClassifierMixin):
    def __init__(self):
        pass

    def fit(self, X, y):
        return self

    def predict(self, X):
        return (np.random.randn(len(X)) > 0).astype(np.int)

    def score(self, X, y):
        return np.mean(self.predict(X) == y)

# Count words in text
# vocabulary, X = count_words(texts)

# # Try to fit, predict and score
# nb = NB()
# nb.fit(X[::2], y[::2])
# print(nb.score(X[1::2], y[1::2]))
