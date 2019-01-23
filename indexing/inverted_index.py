from db import db
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import pymongo
from pymongo import UpdateOne, UpdateMany
from timeit import Timer
from collections import defaultdict
import json

tokenizer = RegexpTokenizer(r'\w+')
index = db["index"]
inverted_index = defaultdict(lambda: defaultdict(list))

arxiv_coll = db['metadata']
cursor = arxiv_coll.find({})

stop = stopwords.words('english')
c = 0
for document in cursor:
    doc = document['_id']
    desc = document['abstract']
    tokens = [t.lower() for t in tokenizer.tokenize(desc)]
    tokens = {word for word in tokens if word not in stop}
    for t in tokens:
        inverted_index[t]['doc'].append(doc)
    c += 1
    print(c)

d = []
data = json.loads(json.dumps(inverted_index))
for k, v in data.items():
    d.append({'_id': k, 'doc': v['doc']})
index.insert_many(d)
