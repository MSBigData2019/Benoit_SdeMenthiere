
# coding: utf-8

# In[1]:


run sentimentanalysis.py


# In[2]:


import math
# from multiprocessing import Pool


# In[3]:


def count_word(text):
    words_text = text.split()
    unique, count = np.unique(words_text, return_counts=True)
    return pd.Series(dict(zip(unique, count)))


# In[4]:


def count_words(texts, count_word=count_word):
    data = map(count_word, texts)
    concat = pd.concat(data, axis = 1, ignore_index=True, sort=False)
    return concat


# In[10]:


class NB(BaseEstimator, ClassifierMixin):
    def __init__(self, count_words=count_words):
        self._count_words = count_words

    def fit(self, texts, y):
        concat = self._count_words(texts)
        self.vocab = {k:v for v, k in enumerate(list(concat.index))}
        V = set(concat.index)
        N = len(texts)
        self.C, counts = np.unique(y, return_counts=True)
        self.prior = {}
        self.condprob = {}
        for classe in self.C:
            Nc = counts[classe]
            self.prior[classe] = Nc / N
            text_c = concat.iloc[:,y==classe]
            count = text_c.sum(axis=1)
            self.condprob[classe] = (count+1)/sum(count+1)
        return V, self.prior, self.condprob

    def _predict_(self, text):
        W = text.split()
        score = {}
        for classe in self.C:
            score[classe]= math.log(self.prior[classe])
            for t in W:
                try:
                    score[classe]+= math.log(self.condprob[classe][self.vocab[t]])
                except:
                    pass
        return max(score, key=score.get)
    
    def predict(self, texts):
        return list(map(self._predict_, texts))

    def score(self, X, y):
        pred = self.predict(X)
        return np.mean( np.array(pred) == np.array(y))


# In[14]:


from sklearn.model_selection import KFold
kf = KFold(n_splits=5, shuffle=True)
SCORE = []
for train_index, test_index in kf.split(range(2000)):
    X_train, X_test = [texts[i] for i in train_index], [texts[i] for i in test_index]
    y_train, y_test = [y[i] for i in train_index], [y[i] for i in test_index]
    nb = NB()
    nb.fit(X_train, y_train)
    SCORE.append(nb.score(X_test, y_test))
    break
print(np.mean(SCORE))


# In[9]:


with open("./34data/data/english.stop", encoding="utf8", mode="r+") as f:
    stop_words = f.read().splitlines()


# In[2]:


def count_word(text):
    words_text = text.split()
    words_without_stop_words = [word for word in words_text if word not in stop_words]
    unique, count = np.unique(words_without_stop_words, return_counts=True)
    return pd.Series(dict(zip(unique, count)))


# In[28]:


from sklearn.model_selection import KFold
kf = KFold(n_splits=5, shuffle=True)
SCORE = []
for train_index, test_index in kf.split(range(2000)):
    X_train, X_test = [texts[i] for i in train_index], [texts[i] for i in test_index]
    y_train, y_test = [y[i] for i in train_index], [y[i] for i in test_index]
    nb = NB()
    nb.fit(X_train, y_train)
    SCORE.append(nb.score(X_test, y_test))
print(np.mean(SCORE))


# In[12]:


from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline


# In[13]:


cv=CountVectorizer('content')


# In[43]:


cv.fit(texts)


# In[42]:


cv.vocabulary


# In[14]:


from sklearn.feature_extraction.text import TfidfTransformer


# In[10]:


from sklearn.linear_model import LogisticRegression


# In[81]:


stemmer = SnowballStemmer('english')


# In[82]:


# CountVectorizer(stop_words=stop_words)
stem_vectorizer = StemmedCountVectorizer(stemmer)


# In[83]:


text_clf = Pipeline([
    ('vect', stem_vectorizer),
    ('tfidf', TfidfTransformer()),
    ('clf', LogisticRegression())
])


# In[84]:


from sklearn.model_selection import KFold
kf = KFold(n_splits=5, shuffle=True)
SCORE = []
for train_index, test_index in kf.split(range(2000)):
    X_train, X_test = [texts[i] for i in train_index], [texts[i] for i in test_index]
    y_train, y_test = [y[i] for i in train_index], [y[i] for i in test_index]
    text_clf.fit(X_train, y_train) 
    SCORE.append(text_clf.score(X_test, y_test))
print(np.mean(SCORE))


# In[18]:


from nltk import SnowballStemmer


# In[73]:


class StemmedCountVectorizer(CountVectorizer):
    def __init__(self, stemmer):
        super(StemmedCountVectorizer, self).__init__()
        self.stemmer = stemmer

    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc:(self.stemmer.stem(w) for w in analyzer(doc))


# In[79]:


class stemmer():
    def __init__(self):
        
        pass
    def fit(self, *args):
        return self
    def transform(self,words):
        stem = SnowballStemmer("english")
        return [stem.stem(word) for word in words]


# In[39]:


stemmer.stem("!")


# In[44]:


def count_word(text):
    words_text = text.split()
    words_stem = [stemmer.stem(word) for word in words_text if word not in stop_words]
    unique, count = np.unique(words_stem, return_counts=True)
    return pd.Series(dict(zip(unique, count)))

