from db import db
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from sklearn.feature_extraction.text import TfidfVectorizer

import pickle
import os
import re


VECTOR_FILE = 'vectors.p'

if os.path.isfile(VECTOR_FILE):
    handle = open(VECTOR_FILE, 'rb')
    ds = pickle.load(handle)
    handle.close()

arxiv = db['metadata']
cursor = arxiv.find({})

tokenizer = RegexpTokenizer(r'\w+')
vectorizer = TfidfVectorizer()
stop = set(stopwords.words('english'))
stemmer = SnowballStemmer('english')
pattern = re.compile(r'\b(' + r'|'.join(stop) + r')\b\s*')

def train():
    c = 0
    abstracts = []
    ids = []
    data_dump = {}

    for document in cursor:
        idx = document['_id']
        abstract = document['abstract']
        tokens = [t.lower() for t in tokenizer.tokenize(abstract)]
        # Index stopwords from now on
        # tokens = {word for word in tokens if word not in stop}
        # tokens = pattern.sub('', ' '.join(tokens))
        # tokens = set(tokens) - stop
        ids.append(idx)
        abstracts.append(' '.join(tokens))
        c += 1

        if c % 10000 == 0:
            print("Processed", c)

    vec = vectorizer.fit_transform(abstracts)
    data_dump['ids'] = ids
    data_dump['vocab'] = vectorizer.vocabulary_
    data_dump['X'] = vec
    data_dump['vectorizer'] = vectorizer
    handle = open(VECTOR_FILE, 'wb')
    pickle.dump(data_dump, handle)
    handle.close()

train()
