# models.py - Custom scikit-learn transformers for email preprocessing and vectorization

from collections import Counter
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import re
from scipy.sparse import csr_matrix
import nltk

# Initialize the Porter stemmer
stemmer = nltk.PorterStemmer()

# Transformer: converts raw text into word count dictionaries
class EmailToWordCounterTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, lower_case=True, remove_punctuation=True,
                 replace_urls=True, replace_numbers=True, stemming=True):
        self.lower_case = lower_case
        self.remove_punctuation = remove_punctuation
        self.replace_urls = replace_urls
        self.replace_numbers = replace_numbers
        self.stemming = stemming

    def fit(self, X, y=None):
        # No fitting required for this transformer
        return self

    def transform(self, X, y=None):
        X_transformed = []
        for text in X:  # expects plain text input
            if self.lower_case:
                text = text.lower()
            if self.replace_numbers:
                text = re.sub(r'\d+(?:\.\d*)?(?:[eE][+-]?\d+)?', 'NUMBER', text)
            if self.remove_punctuation:
                text = re.sub(r'\W+', ' ', text)
            word_counts = Counter(text.split())
            if self.stemming:
                # Stem words to their root forms
                word_counts = Counter({stemmer.stem(w): c for w, c in word_counts.items()})
            X_transformed.append(word_counts)
        return np.array(X_transformed, dtype=object)

# Transformer: converts word count dictionaries into sparse numerical vectors
class WordCounterToVectorTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, vocabulary_size=1000):
        self.vocabulary_size = vocabulary_size

    def fit(self, X, y=None):
        # Build vocabulary of most frequent words across dataset
        total_count = Counter()
        for wc in X:
            for word, count in wc.items():
                total_count[word] += min(count, 10)  # cap counts to avoid dominance
        most_common = total_count.most_common()[:self.vocabulary_size]
        self.vocabulary_ = {word: i+1 for i, (word, _) in enumerate(most_common)}
        return self

    def transform(self, X, y=None):
        rows, cols, data = [], [], []
        for row, wc in enumerate(X):
            for word, count in wc.items():
                rows.append(row)
                cols.append(self.vocabulary_.get(word, 0))  # 0 for unknown words
                data.append(count)
        # Return sparse CSR matrix: shape = (n_samples, vocabulary_size+1)
        return csr_matrix((data, (rows, cols)), shape=(len(X), self.vocabulary_size+1))
